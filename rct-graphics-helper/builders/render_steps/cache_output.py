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

class CacheOutput(RenderStep):
    def __init__(self, input, output, exr):
        self.input = input
        self.exr = exr
        self.output = self.create_output(output)

    def execute(self, context, callback):
        output_magick_command = MagickCommand(self.input["value"])

        file_ext = ".png"
        if self.exr:
            file_ext = ".exr"

        output_path = os.path.join(context.temp_path, "{}{}".format(self.output["value"], file_ext))
        
        magick_str = output_magick_command.get_command_string(
            context.renderer.magick_path, output_path)
        
        subprocess.check_output(magick_str, shell=True)
        
        self.output["value"] = output_path
        print("Writing cached result to {}".format(self.output["value"]))

        return True

