'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from ..builders.spline_builder import SplineBuilder


class TrackInit(bpy.types.Operator):
    bl_idname = "render.rct_track_init"
    bl_label = "Initialize track splines"

    scene = None
    props = None

    def execute(self, context):
        # Create dependencies in the context
        splineBuilder = SplineBuilder()
        splineBuilder.build(context)

        return {'FINISHED'}