'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from ..builders.task_builder import TaskBuilder

from ..operators.render_operator import RCTRender

class TrackProperties(bpy.types.PropertyGroup):
    multi_layer = bpy.props.BoolProperty(
        name="Multi-Layer",
        description="Whether the track needs multiple layers to appear both behind and in front of the vehicle sprites",
        default=False)


def register_track_properties():
    bpy.types.Scene.rct_graphics_helper_track_properties = bpy.props.PointerProperty(
        type=TrackProperties)


def unregister_track_properties():
    del bpy.types.Scene.rct_graphics_helper_track_properties
