'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import traceback

from .properties.preferences import RCTGraphicsHelperPreferences
from .properties.vehicle_properties import register_vehicles_properties, unregister_vehicles_properties
from .properties.tiles_properties import register_tiles_properties, unregister_tiles_properties
from .properties.general_properties import register_general_properties, unregister_general_properties
from .rct_graphics_helper_panel import GraphicsHelperPanel
from . import developer_utils
import importlib
import bpy

bl_info = {
    "name": "RCT Graphics Helper",
    "description": "Render tool to replicate RCT graphics",
    "author": "Olivier Wervers",
    "version": (0, 3, 3),
    "blender": (2, 79, 0),
    "location": "Render",
    "support": "COMMUNITY",
    "category": "Render"}

# load and reload submodules
##################################

importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(
    __path__, __name__, "bpy" in locals())


# register
##################################

def register():
    try:
        bpy.utils.register_module(__name__)
    except:
        traceback.print_exc()

    register_general_properties()
    register_tiles_properties()
    register_vehicles_properties()

    print("Registered {} with {} modules".format(
        bl_info["name"], len(modules)))


def unregister():
    try:
        bpy.utils.unregister_module(__name__)
    except:
        traceback.print_exc()

    unregister_general_properties()
    unregister_tiles_properties()
    unregister_vehicles_properties()

    print("Unregistered {}".format(bl_info["name"]))
