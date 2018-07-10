'''
Copyright (c) 2018 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

class GeneralProperties(bpy.types.PropertyGroup):
    out_start_index = bpy.props.IntProperty(
        name = "Output Starting Index",
        description = "Number to start counting from for the output file names",
        default = 0,
        min = 0)
    
    output_directory = bpy.props.StringProperty(
        name="Output Folder",
        description="Directory to output the sprites to",
        maxlen= 1024,
        subtype='DIR_PATH',
        default= "//output\\")

    
class VehiclesPanel(bpy.types.Panel):
    bl_label = "RCT General"
    bl_idname = "RENDER_PT_rct_general"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        properties = scene.rct_graphics_helper_general_properties

        row = layout.row()
        row.prop(properties, "out_start_index")

        row = layout.row()
        row.prop(properties, "output_directory")

def register_general_panel():
    bpy.types.Scene.rct_graphics_helper_general_properties = bpy.props.PointerProperty(type=GeneralProperties)
    
def unregister_general_panel():
    del bpy.types.Scene.rct_graphics_helper_general_properties
