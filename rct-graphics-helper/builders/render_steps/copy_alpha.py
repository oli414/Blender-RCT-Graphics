'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

from ...magick_command import MagickCommand
from .render_step import RenderStep

class CopyAlpha(RenderStep):
    def __init__(self, input, mask_input, inverted=False):
        self.input = input
        self.mask_input = mask_input
        self.inverted = inverted

        self.output = self.create_output()
    
    def execute(self, context, callback):
        magick_command = MagickCommand(self.input["value"])

        if not self.inverted:
            magick_command.copy_alpha_v2(self.mask_input["value"])
        else:
            magick_command.copy_alpha_inverted_v2(self.mask_input["value"])

        self.output["value"] = magick_command

        return True

