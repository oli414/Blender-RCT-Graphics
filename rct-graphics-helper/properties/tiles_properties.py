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


class TilesProperties(bpy.types.PropertyGroup):
    viewing_angles = bpy.props.IntProperty(
        name="Viewing Angles",
        description="Number of viewing angles to render for.",
        default=4,
        min=1)

    object_width = bpy.props.IntProperty(
        name="Object Width",
        description="Width of the object in tiles. Only used for large scenery.",
        default=1,
        min=1)
    object_length = bpy.props.IntProperty(
        name="Object Length",
        description="Length of the object in tiles. Only used for large scenery.",
        default=1,
        min=1)
     
    invert_tile_positions = bpy.props.BoolProperty(
        name="Invert Tile Positions",
        description="Some large scenery pieces extend into the negative axis, whilst others extends into the positive axis. Use this setting to switch between the two.",
        default=False)


def register_tiles_properties():
    bpy.types.Scene.rct_graphics_helper_static_properties = bpy.props.PointerProperty(
        type=TilesProperties)


def unregister_tiles_properties():
    del bpy.types.Scene.rct_graphics_helper_static_properties
