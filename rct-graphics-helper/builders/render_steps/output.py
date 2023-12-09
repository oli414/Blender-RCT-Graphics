'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import os
import subprocess

from ...magick_command import MagickCommand
from .render_step import RenderStep

class OutputInfo:
    def __init__(self):
        self.path = ""
        self.index = 0
        self.offset_x = 0
        self.offset_y = 0

class Output(RenderStep):
    def __init__(self, input, index=-1, offset_x=0, offset_y=0):
        self.input = input
        self.index = index
        self.offset_x = offset_x
        self.offset_y = offset_y
    
    def execute(self, context, callback):
        if self.index < 0:
            self.index = len(context.task.output_info)

        output_magick_command = MagickCommand(self.input["value"])
        output_magick_command.trim()

        output_path = os.path.join(context.output_path, "sprite_{}.png".format(self.index))
        
        magick_str = output_magick_command.get_command_string(
            context.renderer.magick_path, output_path)
        
        print(magick_str)
        result = str(subprocess.check_output(magick_str, shell=True))

        output_info = self._get_output_info_from_results(
            context, result, self.index, output_path)

        context.task.output_info.append(output_info)

        return True
    
    def _get_output_info_from_results(self, context, result, output_index, output_path):
        output = OutputInfo()
        output.index = output_index
        output.path = output_path

        print(result)
        print(result[2:][:-1])

        if result[2:][:-1] is not "":
            offset_coords = result[2:][:-1].split(" ")

            output.offset_x = int(round(float(offset_coords[0])))
            output.offset_y = int(round(float(offset_coords[1]))) + 15
            
            output.offset_x += self.offset_x
            output.offset_y += self.offset_y

            output.offset_y -= context.renderer.lens_shift_y_offset
            output.offset_y += context.renderer.context.scene.rct_graphics_helper_general_properties.y_offset

        return output

