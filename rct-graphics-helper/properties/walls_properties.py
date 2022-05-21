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


class WallsProperties(bpy.types.PropertyGroup):
    double_sided = bpy.props.BoolProperty(
        name="Double Sided",
        description="Render the wall from four viewing angles. Useful for walls that have more thickness, or differently sided walls.",
        default=False)

    sloped = bpy.props.BoolProperty(
        name="Sloped",
        description="Render the wall for sloped terrain.",
        default=False)

    doorway = bpy.props.BoolProperty(
        name="Doorway",
        description="Render a doorway that vehicles can pass through.",
        default=False)


def register_walls_properties():
    bpy.types.Scene.rct_graphics_helper_walls_properties = bpy.props.PointerProperty(
        type=WallsProperties)


def unregister_walls_properties():
    del bpy.types.Scene.rct_graphics_helper_walls_properties
