'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from .render_operator import RCTRender


class RenderWalls(RCTRender, bpy.types.Operator):
    bl_idname = "render.rct_walls"
    bl_label = "Render RCT Walls"

    def add_slopes_section(self, anim_frame, a_slope_frame_offset, b_slope_frame_offset):
        self.task_builder.set_offset(-14, -8)
        self.task_builder.set_rotation(0)
        self.task_builder.add_viewing_angles(
            1, anim_frame + a_slope_frame_offset)

        self.task_builder.set_offset(15, -7)
        self.task_builder.set_rotation(90)
        self.task_builder.add_viewing_angles(
            1, anim_frame + b_slope_frame_offset)

        self.task_builder.set_offset(-14, -8)
        self.task_builder.set_rotation(0)
        self.task_builder.add_viewing_angles(
            1, anim_frame + b_slope_frame_offset)

        self.task_builder.set_offset(15, -7)
        self.task_builder.set_rotation(90)
        self.task_builder.add_viewing_angles(
            1, anim_frame + a_slope_frame_offset)

    def add_extended_slopes_section(self, anim_frame, a_slope_frame_offset, b_slope_frame_offset):
        self.task_builder.set_offset(-15, -9)
        self.task_builder.set_rotation(180)
        self.task_builder.add_viewing_angles(
            1, anim_frame + b_slope_frame_offset)

        self.task_builder.set_offset(16, -8)
        self.task_builder.set_rotation(270)
        self.task_builder.add_viewing_angles(
            1, anim_frame + a_slope_frame_offset)

        self.task_builder.set_offset(-15, -9)
        self.task_builder.set_rotation(180)
        self.task_builder.add_viewing_angles(
            1, anim_frame + a_slope_frame_offset)

        self.task_builder.set_offset(16, -8)
        self.task_builder.set_rotation(270)
        self.task_builder.add_viewing_angles(
            1, anim_frame + b_slope_frame_offset)

    def add_wall_section(self, anim_frame):
        self.task_builder.set_offset(-14, -8)
        self.task_builder.set_rotation(0)
        self.task_builder.add_viewing_angles(1, anim_frame)

        self.task_builder.set_offset(15, -7)
        self.task_builder.set_rotation(90)
        self.task_builder.add_viewing_angles(1, anim_frame)

    def add_extended_wall_section(self, anim_frame):
        self.task_builder.set_offset(-15, -9)
        self.task_builder.set_rotation(180)
        self.task_builder.add_viewing_angles(1, anim_frame)

        self.task_builder.set_offset(16, -8)
        self.task_builder.set_rotation(270)
        self.task_builder.add_viewing_angles(1, anim_frame)

    def create_task(self, context):
        scene = context.scene
        props = scene.rct_graphics_helper_walls_properties
        general_props = scene.rct_graphics_helper_general_properties

        # Create the list of frames with our parameters
        self.task_builder.clear()
        self.task_builder.set_anti_aliasing_with_background(
            scene.render.use_antialiasing, general_props.anti_alias_with_background, general_props.maintain_aliased_silhouette)
        self.task_builder.set_palette(self.palette_manager.get_base_palette(
            general_props.palette, general_props.number_of_recolorables, "FULL"))
        self.task_builder.set_output_index(general_props.out_start_index)

        self.task_builder.set_recolorables(
            general_props.number_of_recolorables)

        sloped_a_anim_frame = general_props.number_of_animation_frames
        sloped_b_anim_frame = general_props.number_of_animation_frames * 2

        animation_frames = general_props.number_of_animation_frames

        if props.doorway:
            self.task_builder.set_occlusion_layers(2)
            
            self.add_wall_section(0)
            
            for i in range(4):
                self.add_extended_wall_section(1 + i)
                
            for i in range(4):
                self.add_wall_section(1 + i)
            
        else:
            if props.double_sided:
                for animationIndex in range(animation_frames):
                    self.add_extended_wall_section(animationIndex)

                    if props.sloped:
                        self.add_extended_slopes_section(
                            animationIndex, sloped_a_anim_frame, sloped_b_anim_frame)
                if not props.sloped:
                    # Skip some indices to generate blank frames. Double sided walls require the same layout as sloped walls.
                    self.task_builder.set_output_index(
                        general_props.out_start_index + animation_frames * 6)


            for animationIndex in range(animation_frames):
                self.add_wall_section(animationIndex)

                if props.sloped:
                    self.add_slopes_section(
                        animationIndex, sloped_a_anim_frame, sloped_b_anim_frame)

        return self.task_builder.create_task(context)
