'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy

from .vehicle_render_operator import RenderVehicle
from .walls_render_operator import RenderWalls
from .render_tiles_operator import RenderTiles

class RenderRCTSwitch(bpy.types.Operator):
    bl_idname = "render.rct_switch"
    bl_label = "Render RCT project"


    def execute(self, context):
        
        properties = context.scene.rct_graphics_helper_general_properties
        render_mode = properties.render_mode

        if render_mode == "TILES":
            bpy.ops.render.rct_static()
        elif render_mode == "VEHICLE":
            bpy.ops.render.rct_vehicle()
        elif render_mode == "WALLS":
            bpy.ops.render.rct_walls()
        
        return{'FINISHED'}
