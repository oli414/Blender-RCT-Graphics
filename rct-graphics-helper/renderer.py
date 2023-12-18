'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import sched
import time
import faulthandler
import os
import threading
import copy
import bpy

from sys import platform

from .res.res import res_path
from .helpers import find_material_by_name
from .builders.materials_builder import MaterialsBuilder

from .palette_manager import PaletteManager

def find_node_by_label(tree, node_to_find):
    for node in tree.nodes:
        if node.label == node_to_find:
            return node
    return None


class RenderSettings:
    def __init__(self):
        self.aa = True
        self.aa_with_background = True
        self.maintain_aa_silhoutte = False
        self.shadows = True
        self.width = 1
        self.length = 1
        self.floor = -100
        self.layer = "Editor"
        self.frame = 0
        
    def from_general_props(self, general_props):
        self.aa_with_background = general_props.anti_alias_with_background

    def clone(self):
        return copy.deepcopy(self)
    
    def is_oversized(self):
        return self.width > 1 or self.length > 1
    
    def get_frame_output_suffix(self):
        return self.frame.zfill(4)


# Controls the render settings, and starting render processes

class Renderer:
    def __init__(self, context, palette_manager):
        self.context = context

        self.magick_path = os.path.join(res_path, "dependencies", "imagemagick", "magick")

        # If the system platform does not support the included imagemagick version, rely
        # on the path variable instead.
        if platform != "win32":
            self.magick_path = "magick"
        
        self.floyd_steinberg_diffusion = 5

        self.palette_manager = palette_manager

        self.rendering = False
        self.timer = None
        self.render_finished_callback = None

        self.world_position_material = find_material_by_name("WorldPosition")

        self.lens_shift_y_offset = round(bpy.data.cameras["Camera"].shift_y *
                                         context.scene.render.resolution_x)

        self.started_with_anti_aliasing = context.scene.render.use_antialiasing
        context.scene.render.use_shadows = context.scene.rct_graphics_helper_general_properties.cast_shadows

        bpy.app.handlers.render_complete.append(self._render_finished)
        bpy.app.handlers.render_cancel.append(self._render_reset)

    def render_scene_v2(self, output_path, meta_output_path, meta_output_file_name, render_settings, callback):
        self.set_output_path(output_path)
        self.set_meta_output_path(meta_output_path, meta_output_file_name)

        self._apply_render_settings(render_settings)
        
        self.set_override_material(None)

        self.render_finished_callback = callback
        self._render_started()
        bpy.ops.render.render(write_still=True)
        self.render_finished_callback()

    def render_tile_index_map_v2(self, output_path, render_settings, callback):
        self.set_output_path(output_path)
        self.set_meta_output_path(None, None)

        self._apply_render_settings(render_settings)

        self.set_aa_with_background(False)

        world_position_mat = find_material_by_name("WorldPosition")
        self.set_override_material(world_position_mat)

        self.render_finished_callback = callback
        self._render_started()
        bpy.ops.render.render(write_still=True)
        self.render_finished_callback()

    def _apply_render_settings(self, render_settings):
        self.set_aa(render_settings.aa)
        self.set_aa_with_background(render_settings.aa_with_background)
        self.set_layer(render_settings.layer)

    # Render out the current scene
    def render(self, output_still, callback):
        self.context.scene.render.use_compositing = True
        self.render_finished_callback = callback

        self._render_started()

        bpy.ops.render.render(write_still=output_still)  # "INVOKE_DEFAULT"
        self.render_finished_callback()

    def render_composite(self, callback):
        self.context.scene.render.use_compositing = True
        self.render_finished_callback = callback

        self._render_started()

        bpy.ops.render.render(write_still=False)  # "INVOKE_DEFAULT"
        self.render_finished_callback()

    def render_tile_index_map(self, callback):
        self.context.scene.render.use_compositing = True
        self.render_finished_callback = callback
        
        self.context.scene.render.image_settings.file_format = "OPEN_EXR"
        self.context.scene.render.image_settings.color_mode = "RGBA"
        self.context.scene.render.image_settings.color_depth = "16"

        self._render_started()

        bpy.ops.render.render(write_still=True)  # "INVOKE_DEFAULT"
        self.render_finished_callback()

    def _render_started(self):
        if self.rendering:
            return
        
        print("Starting render...")
        self.rendering = True

    def _render_finished(self, _):
        if not self.rendering:
            return

        print("Render Callback: Finished rendering")

        self._render_reset()


    def reset(self):
        self.set_multi_tile_size(1, 1)
        self.set_multi_tile_offset(0, 0)
        self.set_aa(self.started_with_anti_aliasing)
        self.set_aa_with_background(False)
        self.set_override_material(None)
        self.set_layer("Editor")
        self.context.scene.render.image_settings.file_format = "PNG"
        self.context.scene.render.image_settings.color_mode = "RGBA"
        self.context.scene.render.image_settings.color_depth = "8"

    def _render_reset(self, _=None):
        if not self.rendering:
            return

        self.rendering = False
        
        self.reset()

    def _render_finished_safe(self):
        print ("Finished rendering safely")
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
        self.context.scene.render.layers["Track"].material_override = material
        self.context.scene.render.layers["Track Occluded"].material_override = material
        for i in range(8):
            self.context.scene.render.layers["Riders {}".format(
                i + 1)].material_override = material

    def set_multi_tile_offset(self, x, y):
        self.world_position_material = find_material_by_name(
            "WorldPosition")
        
        if self.world_position_material is None:
            raise Exception("WorldPosition material could not be found, please click repair")

        origin_x_node = None
        origin_y_node = None
        for key, value in self.world_position_material.node_tree.nodes.items():
            if value.label == "Origin_x":
                origin_x_node = value
                value.outputs[0].default_value = x
            if value.label == "Origin_y":
                origin_y_node = value
                value.outputs[0].default_value = y
        if origin_x_node is None:
            raise Exception("Origin_y node could not be found, please click repair")
        if origin_y_node is None:
            raise Exception("Origin_x node could not be found, please click repair")

        self.set_override_material(self.world_position_material)

    def set_multi_tile_size(self, width, length, floor=-100):
        self.world_position_material = find_material_by_name(
            "WorldPosition")
        
        if self.world_position_material is None:
            raise Exception("WorldPosition material could not be found, please click repair")

        width_node = None
        length_node = None
        floor_node = None
        for key, value in self.world_position_material.node_tree.nodes.items():
            if value.label == "Width":
                width_node = value
                value.outputs[0].default_value = width
            if value.label == "Length":
                length_node = value
                value.outputs[0].default_value = length
            if value.label == "Floor":
                floor_node = value
                value.outputs[0].default_value = floor
        if width_node is None:
            raise Exception("Width node could not be found, please click repair")
        if length_node is None:
            raise Exception("Length node could not be found, please click repair")
        if floor_node is None:
            raise Exception("Floor node could not be found, please click repair")

    # Sets the active render layer
    def set_layer(self, layer_name):
        layers = ["Editor", "Track", "Track Occluded"]
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
    def set_meta_output_path(self, base=None, path=None):
        # Find the file output node in the compositor to set the output file name and path
        material_index_output_node = find_node_by_label(
            self.context.scene.node_tree, "meta_output")

        if material_index_output_node == None:
            raise Exception(
                "The compositing node tree does not contain an output node for the material index.")
        
        if path is None:
            material_index_output_node.mute = True
        else:
            material_index_output_node.mute = False
            # Set the file name and output path for the mask
            material_index_output_node.base_path = base
            material_index_output_node.file_slots[0].path = path
