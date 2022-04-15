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


class SpriteTrackFlag(object):
    name = ""
    description = ""
    default_value = False
    section_id = None

    def __init__(self, section_id, name, description, default_value):
        self.section_id = section_id
        self.name = name
        self.description = description
        self.default_value = default_value


class VehicleProperties(bpy.types.PropertyGroup):
    sprite_track_flags_list = []

    sprite_track_flags_list.append(SpriteTrackFlag(
        "VEHICLE_SPRITE_FLAG_FLAT",
        "Flat",
        "Render sprites for flat track",
        True))
    sprite_track_flags_list.append(SpriteTrackFlag(
        "VEHICLE_SPRITE_FLAG_GENTLE_SLOPES",
        "Gentle Slopes",
        "Render sprites for gentle sloped track",
        True))
    sprite_track_flags_list.append(SpriteTrackFlag(
        "VEHICLE_SPRITE_FLAG_STEEP_SLOPES",
        "Steep Slopes",
        "Render sprites for steep sloped track",
        False))
    sprite_track_flags_list.append(SpriteTrackFlag(
        "VEHICLE_SPRITE_FLAG_VERTICAL_SLOPES",
        "Vertical Slopes And Invert",
        "Render sprites for vertically sloped track and inverts",
        False))
    sprite_track_flags_list.append(SpriteTrackFlag(
        "VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES",
        "Diagonal Slopes",
        "Render sprites for diagonal slopes",
        False))
    sprite_track_flags_list.append(SpriteTrackFlag(
        "VEHICLE_SPRITE_FLAG_FLAT_BANKED",
        "Flat Banked",
        "Render sprites for flat banked track",
        False))
    sprite_track_flags_list.append(SpriteTrackFlag(
        "SLOPED_TURNS",
        "Gentle Sloped Banked",
        "Render sprites for gently sloped banked track and turns",
        False))
    sprite_track_flags_list.append(SpriteTrackFlag(
        "VEHICLE_SPRITE_FLAG_INLINE_TWISTS",
        "Inline twist",
        "Render sprites for the inline twist element",
        False))
    sprite_track_flags_list.append(SpriteTrackFlag(
        "VEHICLE_SPRITE_FLAG_CORKSCREWS",
        "Corkscrew",
        "Render sprites for corkscrews",
        False))
    sprite_track_flags_list.append(SpriteTrackFlag(
        "VEHICLE_SPRITE_FLAG_CURVED_LIFT_HILL",
        "Curved Lift Hill",
        "Render sprites for a curved lift hill",
        False))

    defaults = []
    for sprite_track_flag in sprite_track_flags_list:
        defaults.append(sprite_track_flag.default_value)

    sprite_track_flags = bpy.props.BoolVectorProperty(
        name="Track Pieces",
        default=defaults,
        description="Which track pieces to render sprites for",
        size=len(sprite_track_flags_list))

    restraint_animation = bpy.props.BoolProperty(
        name="Restraint Animation",
        description="Render with restraint animation. The restrain animation is 3 frames long and starts at frame 1",
        default=False)

    inverted_set = bpy.props.BoolProperty(
        name="Inverted Set",
        description="Used for rides which can invert for an extended amount of time like the flying and lay-down rollercoasters",
        default=False)


def register_vehicles_properties():
    bpy.types.Scene.rct_graphics_helper_vehicle_properties = bpy.props.PointerProperty(
        type=VehicleProperties)


def unregister_vehicles_properties():
    del bpy.types.Scene.rct_graphics_helper_vehicle_properties
