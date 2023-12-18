'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

from ...magick_command import MagickCommand
from .render_step import RenderStep

import subprocess

class SelectTiles(RenderStep):
    def __init__(self, input, tile_meta_input, tiles):
        self.input = input
        self.tile_meta_input = tile_meta_input
        self.tiles = tiles

        self.output = self.create_output()
    
    def execute(self, context, callback):
        magick_command = MagickCommand(self.input["value"])

        if len(self.tiles) > 0:
            cached = False
            previous_mask = None
            for tile in self.tiles:
                tile_index = tile
                if type(tile) != int:
                    tile_index = tile.tile_index

                mask = MagickCommand(self.tile_meta_input["value"])
                if not cached:
                    mask = MagickCommand(self.tile_meta_input["value"])
                    mask.write_to_cache("mask")
                    cached = True
                
                mask.nullify_channels(["Green", "Blue"])
                mask.id_mask(tile_index, 0, 0)

                if type(tile) != int:
                    if tile.quadrants is not None:
                        previous_quadrant_mask = None
                        for quadrant in tile.quadrants:
                            quadrant_mask = MagickCommand("mpr:mask")
                            quadrant_mask.nullify_channels(["Red", "Blue"])
                            quadrant_mask.id_mask(0, quadrant, 0)

                            if previous_quadrant_mask == None:
                                previous_quadrant_mask = quadrant_mask
                            else:
                                previous_quadrant_mask.additive(quadrant_mask)
                        if previous_quadrant_mask is not None:
                            mask.and_mask(previous_quadrant_mask)
                            
                if previous_mask == None:
                    previous_mask = mask
                else:
                    previous_mask.additive(mask)

            if previous_mask is not None:
                floor_mask = MagickCommand(self.tile_meta_input["value"])
                floor_mask.nullify_channels(["Red", "Blue"])
                floor_mask.id_mask(0, 4, 0)
                floor_mask.invert_id_mask()
                previous_mask.and_mask(floor_mask)

                magick_command.mask_mix_self(previous_mask)

        self.output["value"] = magick_command
        return True

