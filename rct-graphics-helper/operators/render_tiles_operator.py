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


class RenderTiles(RCTRender, bpy.types.Operator):
    bl_idname = "render.rct_static"
    bl_label = "Render RCT Static"

    def create_task(self, context):
        scene = context.scene
        props = scene.rct_graphics_helper_static_properties
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

        self.task_builder.set_size(
            props.object_width, props.object_length, props.invert_tile_positions)

        for animationIndex in range(general_props.number_of_animation_frames):
            self.task_builder.add_viewing_angles(
                props.viewing_angles, animationIndex)

        # Add rider peep frames
        self.task_builder.set_recolorables(2)
        self.task_builder.set_palette(self.palette_manager.get_rider_palette())
        for i in range(general_props.number_of_rider_sets):
            self.task_builder.set_layer("Riders {}".format(i + 1))

            for animationIndex in range(general_props.number_of_animation_frames):
                self.task_builder.add_viewing_angles(
                    props.viewing_angles, animationIndex)

        return self.task_builder.create_task(context)
