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
from ..angle_sections.track import sprite_group_metadata, legacy_group_names, legacy_group_metadata, legacy_groups_implied, legacy_group_dependencies, legacy_group_map

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


def CreateSpriteEnum(defaultValue):
    return (
        ("0", "None" + (defaultValue == 0 and " (Default)" or ""), "No sprites rendered", 0),
        ("1", "1" + (defaultValue == 1 and " (Default)" or ""), "1 sprite", 1),
        ("2", "2" + (defaultValue == 2 and " (Default)" or ""), "2 sprites", 2),
        ("4", "4" + (defaultValue == 4 and " (Default)" or ""), "4 sprites (recommended minimum)", 4),
        ("8", "8" + (defaultValue == 8 and " (Default)" or ""), "8 sprites", 8),
        ("16", "16" + (defaultValue == 16 and " (Default)" or ""), "16 sprites", 16),
        ("32", "32" + (defaultValue == 32 and " (Default)" or ""), "32 sprites (RCT2 default)", 32),
        ("64", "64" + (defaultValue == 64 and " (Default)" or ""), "64 sprites  ", 64)
    )

def set_groups_by_legacy_set(self, set):
    for groupname, newgroups in legacy_group_map.items():
        for group in newgroups:
            self[group] = sprite_group_metadata[group][0] * (groupname in set)

# this is called with self as VehicleProperties
def legacy_groups_set(self, value):
    new_with_implied = { legacy_group_names[i] for i in range(len(value)) if value[i] or (legacy_group_names[i] in legacy_groups_implied) }
    new = { legacy_group_names[i] for i in range(len(value)) if value[i] and not legacy_group_names[i] in legacy_groups_implied }
    for implied, dependencies in legacy_group_dependencies.items():
        if implied.issubset(new_with_implied):
            for group in dependencies:
                new.add(group)
        if not implied.issubset(new_with_implied) and len(implied) == 1:
            for group in implied:
                new.discard(group)
    set_groups_by_legacy_set(self, new)
    value = [group in new for group in legacy_group_names]
    for i in range(len(value)):
        self.sprite_track_flags[i] = value[i]

def legacy_flags_get(self):
    return [x for x in self.sprite_track_flags]

# When the user switches from full to simple mode, force the groups to match the simple mode
def sprite_group_mode_updated(self, context):
    if self.sprite_group_mode == "SIMPLE":
        set_groups_by_legacy_set(self, self.get_legacy_set())

class VehicleProperties(bpy.types.PropertyGroup):
    # Create legacy sprite groups
    legacy_defaults = []
    legacy_spritegroups = {}
    for legacy_group_name in legacy_group_names:
        config = legacy_group_metadata[legacy_group_name]
        legacy_spritegroups[legacy_group_name] = SpriteTrackFlag(legacy_group_name, *config)
        legacy_defaults.append(config[2])

    sprite_track_flags = bpy.props.BoolVectorProperty(
        name="Track Pieces",
        default=legacy_defaults,
        description="Which track pieces to render sprites for",
        size=len(legacy_spritegroups)
    )
    
    legacy_flags = bpy.props.BoolVectorProperty(
        name="Track Pieces",
        default=legacy_defaults,
        description="Which track pieces to render sprites for",
        size=len(legacy_spritegroups),
        set = legacy_groups_set,
        get = legacy_flags_get
    )

    # Create modern sprite groups
    for key, config in sprite_group_metadata.items():
        locals()[key] = bpy.props.EnumProperty(
            name = key,
            description = config[1],
            items = CreateSpriteEnum(config[0])
        )

    inverted_set = bpy.props.BoolProperty(
        name="Inverted Set",
        description="Used for rides which can invert for an extended amount of time like the flying and lay-down rollercoasters",
        default=False)

    sprite_group_mode = bpy.props.EnumProperty(
        name="Sprite group mode",
        items=(
            ("SIMPLE", "Simple sprite groups",
             "Combines several sprite groups and sets their sprite precisions automatically", 1),
            ("FULL", "Full sprite groups",
             "Set all sprite group precisions manually", 2),
        ),
        update = sprite_group_mode_updated
    )

    def get_legacy_set(self):
        return { legacy_group_names[i] for i in range(len(self.sprite_track_flags)) if self.sprite_track_flags[i] }



def register_vehicles_properties():
    bpy.types.Scene.rct_graphics_helper_vehicle_properties = bpy.props.PointerProperty(
        type=VehicleProperties)


def unregister_vehicles_properties():
    del bpy.types.Scene.rct_graphics_helper_vehicle_properties
