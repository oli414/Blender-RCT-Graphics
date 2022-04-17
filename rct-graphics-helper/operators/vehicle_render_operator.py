'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from ..operators.render_operator import RCTRender
from ..angle_sections.track import track_angle_sections, track_angle_sections_names


class RenderVehicle(RCTRender, bpy.types.Operator):
    bl_idname = "render.rct_vehicle"
    bl_label = "Render RCT Vehicle"

    def create_task(self, context):
        props = context.scene.rct_graphics_helper_vehicle_properties
        general_props = context.scene.rct_graphics_helper_general_properties

        self.task_builder.clear()
        self.task_builder.set_anti_aliasing_with_background(
            context.scene.render.use_antialiasing, general_props.anti_alias_with_background, general_props.maintain_aliased_silhouette)
        self.task_builder.set_output_index(general_props.out_start_index)
        self.task_builder.set_size(1, 1)

        # Add vehicle frames
        self.task_builder.set_recolorables(
            general_props.number_of_recolorables)
        self.task_builder.set_palette(self.palette_manager.get_base_palette(
            general_props.palette, general_props.number_of_recolorables, "VEHICLE"))

        self.add_render_angles(
            context, False, general_props.number_of_animation_frames)

        if props.inverted_set:
            self.add_render_angles(
                context, True, general_props.number_of_animation_frames)

        # Add rider peep frames
        self.task_builder.set_recolorables(2)
        self.task_builder.set_palette(self.palette_manager.get_rider_palette())
        for i in range(general_props.number_of_rider_sets):
            self.task_builder.set_layer("Riders {}".format(i + 1))

            self.add_render_angles(
                context, False, general_props.number_of_animation_frames)

            if props.inverted_set:
                self.add_render_angles(
                    context, True, general_props.number_of_animation_frames)

        return self.task_builder.create_task(context)

    def key_is_property(self, key, props):
        for sprite_track_flagset in props.sprite_track_flags_list:
            if sprite_track_flagset.section_id == key:
                return True

    def property_value(self, key, props):
        i = 0
        for sprite_track_flagset in props.sprite_track_flags_list:
            if sprite_track_flagset.section_id == key:
                return props.sprite_track_flags[i]
            i += 1

    def should_render_feature(self, key, context):
        props = context.scene.rct_graphics_helper_vehicle_properties

        inverted = False
        if self.key_is_property(key, props):
            if self.property_value(key, props):
                return True
        elif key == "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TURNS" or key == "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TRANSITIONS":
            if self.property_value("SLOPED_TURNS", props):
                return True
        elif key == "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_WHILE_BANKED_TRANSITIONS":
            if self.property_value("SLOPED_TURNS", props) and self.property_value("VEHICLE_SPRITE_FLAG_FLAT_BANKED", props):
                return True
        elif key == "VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS":
            if self.property_value("VEHICLE_SPRITE_FLAG_FLAT_BANKED", props) and self.property_value("VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES", props):
                return True
        elif key == "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_BANKED_TRANSITIONS":
            if self.property_value("VEHICLE_SPRITE_FLAG_FLAT_BANKED", props) and self.property_value("VEHICLE_SPRITE_FLAG_GENTLE_SLOPES", props):
                return True
        elif key == "VEHICLE_SPRITE_FLAG_RESTRAINT_ANIMATION" and inverted == False:
            if props.restraint_animation:
                return True
        return False

    def add_render_angles(self, context, is_inverted=False, animation_frames=1):
        extra_roll = 0
        if is_inverted:
            extra_roll = 180

        for i in range(len(track_angle_sections_names)):
            key = track_angle_sections_names[i]
            if self.should_render_feature(key, context):
                track_sections = track_angle_sections[key]
                for track_section in track_sections:

                    base_view_angle = 0
                    if track_section[0]:
                        base_view_angle = 45
                    self.task_builder.set_rotation(
                        base_view_angle, -track_section[3] - extra_roll, track_section[2], track_section[4])

                    if key == "VEHICLE_SPRITE_FLAG_RESTRAINT_ANIMATION":
                        for j in range(3):
                            for k in range(track_section[1]):
                                for l in range(animation_frames):
                                    self.task_builder.set_rotation(
                                        base_view_angle + k / track_section[1] * 360, -track_section[3] - extra_roll, track_section[2], track_section[4])
                                    self.task_builder.add_viewing_angles(
                                        1, animation_frames + j, 1)
                    else:
                        self.task_builder.add_viewing_angles(
                            track_section[1], 0, animation_frames)

    def OLD_append_angles_to_rendertask(self, render_layer, inverted):
        start_anim = 0
        """
        if self.scene.rct_graphics_helper_general_properties.number_of_animation_frames != 1:
            start_anim = 4
        anim_count = self.scene.rct_graphics_helper_general_properties.number_of_animation_frames
        for i in range(len(track_angle_sections_names)):
            key = track_angle_sections_names[i]
            track_section = track_angle_sections[key]
            if self.key_is_property(key):
                if self.property_value(key):
                    self.renderTask.add(
                        track_section, render_layer, inverted, start_anim, anim_count)
            elif key == "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TURNS" or key == "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TRANSITIONS":
                if self.property_value("SLOPED_TURNS"):
                    self.renderTask.add(
                        track_section, render_layer, inverted, start_anim, anim_count)
            elif key == "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_WHILE_BANKED_TRANSITIONS":
                if self.property_value("SLOPED_TURNS") and self.property_value("VEHICLE_SPRITE_FLAG_FLAT_BANKED"):
                    self.renderTask.add(
                        track_section, render_layer, inverted, start_anim, anim_count)
            elif key == "VEHICLE_SPRITE_FLAG_DIAGONAL_GENTLE_SLOPE_BANKED_TRANSITIONS":
                if self.property_value("SLOPED_TURNS") and self.property_value("VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES"):
                    self.renderTask.add(
                        track_section, render_layer, inverted, start_anim, anim_count)
            elif key == "VEHICLE_SPRITE_FLAG_FLAT_TO_GENTLE_SLOPE_BANKED_TRANSITIONS":
                if self.property_value("VEHICLE_SPRITE_FLAG_FLAT_BANKED") and self.property_value("VEHICLE_SPRITE_FLAG_GENTLE_SLOPES"):
                    self.renderTask.add(
                        track_section, render_layer, inverted, start_anim, anim_count)
            elif key == "VEHICLE_SPRITE_FLAG_RESTRAINT_ANIMATION" and inverted == False:
                if self.props.restraint_animation:
                    self.renderTask.add(
                        track_section, render_layer, inverted, 1, 3)
        """
