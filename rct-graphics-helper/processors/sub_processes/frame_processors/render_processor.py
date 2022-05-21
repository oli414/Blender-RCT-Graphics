'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

from ..sub_processor import SubProcessor

# Frame processor for rendering the scene


class RenderProcessor(SubProcessor):
    def __init__(self, renderer):
        super().__init__()

        self.renderer = renderer

    def process(self, frame, callback):
        frame.prepare_scene()

        meta_render_output_folder = frame.task.get_temporary_output_folder()
        meta_render_output_file = frame.get_meta_render_output_file_name("aa_")
        render_output = frame.get_base_render_output_path()

        # Render the main still and meta image
        self.renderer.set_layer(frame.layer)
        self.renderer.set_meta_output_path(
            meta_render_output_folder, meta_render_output_file)
        self.renderer.set_output_path(render_output)

        self.renderer.set_override_material(None)

        self.renderer.set_aa(frame.use_anti_aliasing)
        self.renderer.set_aa_with_background(frame.anti_alias_with_background)

        self.renderer.set_animation_frame(frame.animation_frame_index)

        self.renderer.render(True, callback)

        # Render a meta image without anti-aliasing that we can use as a mask for the alpha later
        # We can skip this step if the image is oversized as that will already render an un-aliased tile-index image
        if frame.maintain_aliased_silhouette and not frame.oversized:
            self.renderer.set_aa(False)
            self.renderer.set_layer(frame.layer)

            naa_meta_render_output = frame.get_meta_render_output_file_name(
                "naa_")
            self.renderer.set_meta_output_path(
                meta_render_output_folder, naa_meta_render_output)

            self.renderer.set_override_material(None)

            self.renderer.set_animation_frame(frame.animation_frame_index)
            self.renderer.render(False, callback)
