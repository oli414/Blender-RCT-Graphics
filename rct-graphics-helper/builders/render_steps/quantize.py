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

class Quantize(RenderStep):
    def __init__(self, input, palette, mai_input=None, recolorables=0):
        self.palette = palette
        self.input = input

        self.mai_input = mai_input
        self.recolorables = recolorables

        self.output = self.create_output()
    
    def execute(self, context, callback):
        magick_command = MagickCommand(self.input["value"])

        if (self.mai_input is not None and self.recolorables > 0):
            magick_command.write_to_cache("prequantize")
        
        magick_command.quantize(context.renderer.get_palette_path(
            self.palette), context.renderer.floyd_steinberg_diffusion)
        
        # If specified, render each recolorable seperately, and combine the results
        if (self.mai_input is not None and self.recolorables > 0):
            # Force the recolorables to a palette that only contains the recolorable color
            channels_to_exclude_for_mai = ["Green", "Blue"]

            for i in range(self.recolorables):
                mask = MagickCommand(self.mai_input["value"])
                mask.nullify_channels(channels_to_exclude_for_mai)
                mask.id_mask(i + 1, 0, 0)

                palette = context.renderer.palette_manager.get_recolor_palette(i)
                orct2_palette = context.renderer.palette_manager.get_orct2_recolor_palette(
                    i)

                forced_color_render = MagickCommand("mpr:prequantize")
                forced_color_render.quantize(context.renderer.get_palette_path(
                    palette), context.renderer.floyd_steinberg_diffusion)

                if i == 0:
                    # Replace our clover green recolor 1 with the OpenRCT2 orange recolor 1
                    forced_color_render.replace_color("#003F21", "#6F332F")
                    forced_color_render.replace_color("#00672F", "#83372F")
                    forced_color_render.replace_color("#0B7B41", "#973F33")
                    forced_color_render.replace_color("#178F51", "#AB4333")
                    forced_color_render.replace_color("#1FA35C", "#BF4B2F")
                    forced_color_render.replace_color("#27B768", "#D34F2B")
                    forced_color_render.replace_color("#3BDB7F", "#E75723")
                    forced_color_render.replace_color("#5BEF98", "#FF5F1F")
                    forced_color_render.replace_color("#77F3A9", "#FF7F27")
                    forced_color_render.replace_color("#97F7BE", "#FF9B33")
                    forced_color_render.replace_color("#B7FBD0", "#FFB73F")
                    forced_color_render.replace_color("#D7FFE5", "#FFCF4B")

                magick_command.mask_mix(forced_color_render, mask)

        self.output["value"] = magick_command

        return True

