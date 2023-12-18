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

class RenderTileIndices(RenderStep):
    def __init__(self, output, render_props, width, length, offset_x=0, offset_y=0, floor=-100):
        self.output = self.create_output(output)
        self.render_props = render_props
        self.width = width
        self.length = length
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.floor=floor

    def execute(self, context, callback):
        name = self.output["value"]
        
        naa_output_name = name + "_ti_naa.exr"
        aa_output_name = name + "_ti_aa.exr"
        naa_output_path = os.path.join(context.temp_path, naa_output_name)
        aa_output_path = os.path.join(context.temp_path, aa_output_name)

        self.output["value"] = naa_output_path

        def finalize():
            merged_output_name = name + "_ti_merged.exr"
            merged_output_path = os.path.join(context.temp_path, merged_output_name)

            aa_mask = MagickCommand(aa_output_path)
            naa_mask = MagickCommand(naa_output_path)
            aa_mask.combine(naa_mask)

            magick_str = aa_mask.get_command_string(
                context.renderer.magick_path, merged_output_path)
            subprocess.check_output(magick_str, shell=True)

            self.output["value"] = merged_output_path
            callback()

        def next():
            if self.render_props.aa:
                context.renderer.set_multi_tile_size(self.width, self.length, self.floor)
                context.renderer.set_multi_tile_offset(self.offset_x, self.offset_y)

                context.renderer.set_aa(True)
                context.renderer.set_aa_with_background(False)
                
                context.renderer.set_output_path(aa_output_path)
                context.renderer.set_meta_output_path(None, None)
                context.renderer.render_tile_index_map(finalize)
            else:
                callback()

        context.renderer.set_multi_tile_size(self.width, self.length, self.floor)
        context.renderer.set_multi_tile_offset(self.offset_x, self.offset_y)

        context.renderer.set_aa(False)
        context.renderer.set_aa_with_background(False)

        context.renderer.set_output_path(naa_output_path)
        context.renderer.set_meta_output_path(None, None)
        context.renderer.render_tile_index_map(next)

        return False

