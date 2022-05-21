'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import subprocess
from ....magick_command import MagickCommand
from ..sub_processor import SubProcessor

# Frame processor for merging the tile index meta images with the material index meta image


class MergeMasksProcessor(SubProcessor):
    def __init__(self, renderer):
        super().__init__()

        self.renderer = renderer

    def applicable(self, frame):
        return True

    def process(self, frame, callback=None):
        tile_index_naa_meta_output = frame.get_meta_render_output_path(
            "ti_naa_")
        tile_index_aa_meta_output = frame.get_meta_render_output_path("ti_aa_")

        main_meta_input = frame.get_meta_render_output_path("aa_")
        main_meta_output = frame.get_meta_render_output_path()

        material_indices = MagickCommand(main_meta_input)

        material_indices.nullify_channels(["Green"])

        if frame.oversized:
            tile_indices = MagickCommand(tile_index_naa_meta_output)
            tile_indices.write_to_cache("ti_naa")

            if frame.use_anti_aliasing:
                merged_tile_indices = MagickCommand(tile_index_aa_meta_output)
                merged_tile_indices.combine(tile_indices)

                tile_indices = merged_tile_indices

            tile_indices.nullify_channels(["Red", "Blue"])

            material_indices.additive(tile_indices)

            if frame.maintain_aliased_silhouette:
                material_indices.copy_alpha("mpr:ti_naa")
        else:
            if frame.maintain_aliased_silhouette:
                naa_meta_output = frame.get_meta_render_output_path(
                    "naa_")
                material_indices.copy_alpha(naa_meta_output)

        result = str(subprocess.check_output(material_indices.get_command_string(
            self.renderer.magick_path, main_meta_output), shell=True))
