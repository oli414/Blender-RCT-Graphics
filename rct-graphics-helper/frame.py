'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

# Representation of a frame that is to be rendered


class Frame:
    def __init__(self, frame_index, task, view_angle, bank_angle=0, vertical_angle=0, mid_angle=0):
        self.frame_index = frame_index
        self.output_indices = [frame_index]

        self.task = task
        self.view_angle = view_angle
        self.bank_angle = bank_angle
        self.vertical_angle = vertical_angle
        self.mid_angle = mid_angle

        self.width = 1
        self.length = 1
        self.oversized = False
        self.invert_tile_positions = False

        self.recolorables = 0

        self.layer = "Editor"

        self.animation_frame_index = 0

        self.occlusion_layers = 0

        self.use_anti_aliasing = True
        self.anti_alias_with_background = False
        self.maintain_aliased_silhouette = True

        self.offset_x = 0
        self.offset_y = 0

        self.base_palette = None

    def get_meta_render_output_path(self, suffix=""):
        file_name = self.get_meta_render_output_file_name(suffix)
        if suffix != "":
            appended_frame_index = str(self.animation_frame_index).zfill(4)
            return os.path.join(self.task.get_temporary_output_folder(), "{}{}.exr".format(file_name, appended_frame_index))
        else:
            return os.path.join(self.task.get_temporary_output_folder(), "{}.mpc".format(file_name))

    def get_meta_render_output_file_name(self, suffix=""):
        if suffix != "":
            return "meta_render_{}_{}_".format(self.frame_index, suffix)
        else:
            return "meta_render_{}".format(self.frame_index)

    def get_base_render_output_path(self):
        return os.path.join(self.task.get_temporary_output_folder(), "render_{}.png".format(self.frame_index))

    def get_quantized_render_output_path(self):
        return os.path.join(self.task.get_temporary_output_folder(), "quantized_{}.png".format(self.frame_index))

    def get_final_output_paths(self):
        if self.oversized or self.occlusion_layers > 0:
            output_paths = []
            for output_index in self.output_indices:
                output_paths.append(os.path.join(
                    self.task.get_output_folder(), "sprites", "sprite_{}.png".format(output_index)))
            return output_paths
        else:
            return [os.path.join(self.task.get_output_folder(), "sprites", "sprite_{}.png".format(self.frame_index))]

    def prepare_scene(self):
        object = bpy.data.objects['Rig']
        if object is None:
            return
        object.rotation_euler = (math.radians(self.bank_angle),
                                 math.radians(self.vertical_angle), math.radians(self.mid_angle))
        vJoint = object.children[0]
        vJoint.rotation_euler = (0, 0, math.radians(self.view_angle - 45))

    def set_anti_aliasing_with_background(self, use_anti_aliasing, anti_alias_with_background, maintain_aliased_silhouette):
        self.use_anti_aliasing = use_anti_aliasing

        # No need to anti-alias with background if anti-aliasing is disabled
        self.anti_alias_with_background = anti_alias_with_background and use_anti_aliasing

        # Always maintain aliased silhouttes when anti-aliasing with the background is disabled
        self.maintain_aliased_silhouette = ((
            not anti_alias_with_background) or maintain_aliased_silhouette) and use_anti_aliasing

    def set_offset(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y

    def set_multi_tile_size(self, width, length, invert_tile_positions):
        self.width = width
        self.length = length

        self.oversized = self.width > 1 or self.length > 1
        if self.oversized:
            self.invert_tile_positions = invert_tile_positions

    def set_layer(self, layer_name):
        self.layer = layer_name

    def set_recolorables(self, number_of_recolorables):
        self.recolorables = number_of_recolorables

    def set_base_palette(self, palette):
        self.base_palette = palette

    def set_occlusion_layers(self, layers):
        self.occlusion_layers = layers

    def set_output_indices(self, indices):
        self.output_indices = indices

        layers = self.occlusion_layers
        if layers == 0:
            layers = 1
        if len(self.output_indices) != self.width * self.length * layers:
            raise Exception(
                "The number of output indices does not match the number of expected output sprites for this frame")
