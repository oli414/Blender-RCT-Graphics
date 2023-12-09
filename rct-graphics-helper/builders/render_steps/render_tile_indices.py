'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import os

from ...magick_command import MagickCommand
from .render_step import RenderStep

class RenderTileIndices(RenderStep):
    def __init__(self, output, render_props, width, length, offset_x=0, offset_y=0):
        self.output = self.create_output(output)
        self.render_props = render_props
        self.width = width
        self.length = length
        self.offset_x = offset_x
        self.offset_y = offset_y

    def execute(self, context, callback):
        name = self.output["value"]
        
        naa_output_name = name + "_ti_naa"
        aa_output_name = name + "_ti_aa"
        naa_output_path = os.path.join(context.temp_path, naa_output_name)
        aa_output_path = os.path.join(context.temp_path, aa_output_name)
        full_naa_path = naa_output_path + "0000.exr"
        full_aa_path = aa_output_path + "0000.exr"

        self.output["value"] = full_naa_path

        def finalize():
            # context.renderer.set_override_material(None)
            aa_mask = MagickCommand(full_aa_path)
            naa_mask = MagickCommand(full_naa_path)
            aa_mask.combine(naa_mask)

            self.output["value"] = aa_mask
            callback()

        def next():
            if self.render_props.aa and self.render_props.aa_with_background:
                context.renderer.set_multi_tile_size(self.width, self.length)
                context.renderer.set_multi_tile_offset(self.offset_x, self.offset_y)

                context.renderer.set_aa(True)
                context.renderer.set_aa_with_background(True)
                
                context.renderer.set_meta_output_path(context.temp_path, aa_output_name)
                context.renderer.render_composite(finalize)
            else:
                callback()

        context.renderer.set_multi_tile_size(self.width, self.length)
        context.renderer.set_multi_tile_offset(self.offset_x, self.offset_y)

        context.renderer.set_aa(False)
        context.renderer.set_aa_with_background(False)

        context.renderer.set_meta_output_path(context.temp_path, naa_output_name)
        context.renderer.render_composite(next)

        return False

