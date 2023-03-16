'''
Copyright (c) 2023 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from ..operators.render_operator import RCTRender
from ..angle_sections.track import sprite_group_names, sprite_group_manifest


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

    def add_render_angles(self, context, is_inverted=False, animation_frames=1):
        properties = context.scene.rct_graphics_helper_vehicle_properties
        extra_roll = 0
        if is_inverted:
            extra_roll = 180

        for sprite_group_name in sprite_group_names:
            track_sections = sprite_group_manifest[sprite_group_name]

            if sprite_group_name not in properties:
                continue
            precision = int(properties[sprite_group_name])
            if precision == 0:
                continue

            for track_section in track_sections:
                # If the sprite angle is intended to be diagonal, offset by 45 degrees unless diagonal sprites will be present
                base_view_angle = 0
                if track_section[0] and precision < 8:
                    base_view_angle = 45

                self.task_builder.set_rotation(
                    base_view_angle, -track_section[3] + extra_roll, track_section[2], track_section[4])

                if sprite_group_name == "restraintAnimation":
                    for j in range(3):
                        for k in range(precision):
                            for l in range(animation_frames):
                                self.task_builder.set_rotation(
                                    base_view_angle + k / precision * 360, -track_section[3] + extra_roll, track_section[2], track_section[4])
                                self.task_builder.add_viewing_angles(
                                    1, animation_frames + j, 1)
                else:
                    self.task_builder.add_viewing_angles(
                        precision, 0, animation_frames)
