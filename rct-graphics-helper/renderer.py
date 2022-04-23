'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import faulthandler
import os
import threading
import bpy

from .builders.materials_builder import MaterialsBuilder

from .palette_manager import PaletteManager


def find_material_by_name(material_name):
    for mat in bpy.data.materials:
        if mat.name == material_name:
            return mat
    return None


def find_node_by_label(tree, node_to_find):
    for node in tree.nodes:
        if node.label == node_to_find:
            return node
    return None

# Model for controlling the render settings, and starting render processes


class Renderer:
    def __init__(self, context, palette_manager):
        self.context = context

        self.magick_path = "magick"
        self.floyd_steinberg_diffusion = 5

        self.palette_manager = palette_manager

        self.rendering = False
        self.timer = None
        self.render_finished_callback = None

        self.world_position_material = find_material_by_name("WorldPosition")

        if self.world_position_material == None:
            materials_builder = MaterialsBuilder()
            materials_builder.create_world_position_material(context)
            self.world_position_material = find_material_by_name(
                "WorldPosition")

        self.lens_shift_y_offset = round(bpy.data.cameras["Camera"].shift_y *
                                         context.scene.render.resolution_x)

        self.started_with_anti_aliasing = context.scene.render.use_antialiasing
        context.scene.render.use_shadows = context.scene.rct_graphics_helper_general_properties.cast_shadows

        bpy.app.handlers.render_complete.append(self._render_finished)
        bpy.app.handlers.render_cancel.append(self._render_reset)

    # Render out the current scene
    def render(self, output_still, callback):
        self.render_finished_callback = callback

        self._render_started()

        bpy.ops.render.render(write_still=output_still)  # "INVOKE_DEFAULT"

    def _render_started(self):
        if self.rendering:
            return

        print("Starting render...")
        self.rendering = True

    def _render_finished(self, _):
        if not self.rendering:
            return

        print("Finished rendering")

        # Start a timer before calling the callback as the render operator takes a bit to fully finish
        #self.timer = threading.Timer(0.01, self._render_finished_safe)
        # self.timer.start()

        print("Reset renderer")
        self._render_reset()
        print("Call callback")
        if self.render_finished_callback != None:
            self.render_finished_callback()

    def _render_reset(self, _=None):
        if not self.rendering:
            return

        self.rendering = False

        self.set_aa(self.started_with_anti_aliasing)
        self.set_aa_with_background(False)
        self.set_override_material(None)
        self.set_layer("Editor")

    def _render_finished_safe(self):
        self.timer.cancel()

        callback = self.render_finished_callback

        self._render_reset()
        if callback != None:
            callback()

    def get_palette_path(self, palette):
        palette.prepare(self)
        return palette.path

    # Enabled or disables anti-aliasing for the next render
    def set_aa(self, aa):
        self.context.scene.render.use_antialiasing = aa

    # Enabled or disables anti-aliasing with the background
    def set_aa_with_background(self, aa_with_background):
        aa_with_backgound_mix_node = find_node_by_label(
            self.context.scene.node_tree, "aa_with_backgound_switch")

        if aa_with_backgound_mix_node == None:
            raise Exception(
                "The compositing node tree does not contain a mix node for anti-aliasing with the background.")

        if aa_with_background:
            aa_with_backgound_mix_node.inputs[0].default_value = 1
        else:
            aa_with_backgound_mix_node.inputs[0].default_value = 0

    # Sets the global override material that the scene is rendered with
    def set_override_material(self, material):
        self.context.scene.render.layers["Editor"].material_override = material
        for i in range(8):
            self.context.scene.render.layers["Riders {}".format(
                i + 1)].material_override = material

    # Sets the active render layer
    def set_layer(self, layer_name):
        layers = ["Editor"]
        for i in range(8):
            layers.append("Riders {}".format(i + 1))
        for layer in layers:
            self.context.scene.render.layers[layer].use = False
        self.context.scene.render.layers[layer_name].use = True

        input_layer_node = find_node_by_label(
            self.context.scene.node_tree, "input_layer")

        if input_layer_node == None:
            raise Exception(
                "The compositing node tree does not contain an input layer node.")

        input_layer_node.layer = layer_name

    def set_animation_frame(self, animation_frame_index):
        self.context.scene.frame_set(animation_frame_index)

    # Sets the still render output path
    def set_output_path(self, path):
        self.context.scene.render.filepath = path

    # Sets the meta (material and tile mask) render output path
    def set_meta_output_path(self, base, path):
        # Find the file output node in the compositor to set the output file name and path
        material_index_output_node = find_node_by_label(
            self.context.scene.node_tree, "meta_output")

        if material_index_output_node == None:
            raise Exception(
                "The compositing node tree does not contain an output node for the material index.")

        # Set the file name and output path for the mask
        material_index_output_node.base_path = base
        material_index_output_node.file_slots[0].path = path
