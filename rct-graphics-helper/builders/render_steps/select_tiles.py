'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

from ...magick_command import MagickCommand
from .render_step import RenderStep

class SelectTiles(RenderStep):
    def __init__(self, input, tile_meta_input, tiles):
        self.input = input
        self.tile_meta_input = tile_meta_input
        self.tiles = tiles

        self.output = self.create_output()
    
    def execute(self, context, callback):
        magick_command = MagickCommand(self.input["value"])

        if len(self.tiles) > 0:
            master_mask = MagickCommand(self.tile_meta_input["value"])
            master_mask.nullify_channels(["Red", "Blue"])
            master_mask.write_to_cache("mask")
            master_mask.id_mask(0, self.tiles[0], 0)

            first_it = True
            for tile_index in self.tiles:
                if first_it:
                    first_it = False
                    continue

                mask = MagickCommand("mpr:mask")
                mask.id_mask(0, tile_index, 0)

                master_mask.additive(mask)
            
            magick_command.mask_mix_self(master_mask)

        self.output["value"] = magick_command
        return True

