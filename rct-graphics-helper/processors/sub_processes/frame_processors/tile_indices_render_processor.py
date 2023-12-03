'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

from ..sub_processor import SubProcessor

# Frame processor for rendering the scene with the world position material to generate the tile index meta image


class TileIndicesRenderProcessor(SubProcessor):
    def __init__(self, renderer, with_anti_aliasing):
        super().__init__()

        self.is_async = False

        self.with_anti_aliasing = with_anti_aliasing

        self.renderer = renderer

    def applicable(self, frame):
        if not frame.oversized:
            return False

        if self.with_anti_aliasing:
            return frame.use_anti_aliasing
        else:
            return True

    def process(self, frame, callback):
        frame.prepare_scene()

        output_suffix = "ti_"

        if self.with_anti_aliasing:
            output_suffix = "ti_aa_"
        else:
            output_suffix = "ti_naa_"

        meta_render_output = frame.get_meta_render_output_file_name(
            output_suffix)

        if frame.oversized:
            self.renderer.set_multi_tile_size(frame.width, frame.length)
        else:
            self.renderer.set_multi_tile_size(1, 1)
        self.renderer.set_layer(frame.layer)
        self.renderer.set_aa(self.with_anti_aliasing)
        self.renderer.set_meta_output_path(
            frame.task.get_temporary_output_folder(), meta_render_output)

        self.renderer.set_override_material(
            self.renderer.world_position_material)

        self.renderer.set_animation_frame(frame.animation_frame_index)

        self.renderer.render(False, callback)
