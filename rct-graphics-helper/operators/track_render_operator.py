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


class RenderTrack(RCTRender, bpy.types.Operator):
    bl_idname = "render.rct_track"
    bl_label = "Render RCT Track"

    def create_task(self, context):
        scene = context.scene
        props = scene.rct_graphics_helper_track_properties
        general_props = scene.rct_graphics_helper_general_properties

        # Create the list of frames with our parameters
        self.task_builder.clear()
        return self.task_builder.create_task(context)
