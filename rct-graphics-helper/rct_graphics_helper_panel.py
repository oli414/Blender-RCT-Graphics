'''
Copyright (c) 2023 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from .operators.init_operator import Init

from .operators.vehicle_render_operator import RenderVehicle

from .operators.walls_render_operator import RenderWalls

from .operators.render_tiles_operator import RenderTiles

from .models.palette import palette_colors, palette_colors_details
from .angle_sections.track import sprite_group_names, legacy_group_names

class GraphicsHelperPanel(bpy.types.Panel):

    bl_label = "RCT Graphics Helper"
    bl_idname = "VIEW3D_PT_rct_graphics_helper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'RCT Tools'

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.operator("render.rct_init", text="Initialize / Repair")

        if not "Rig" in context.scene.objects:
            return

        # General properties

        properties = scene.rct_graphics_helper_general_properties

        row = layout.row()
        row.separator()

        row = layout.row()
        row.label("General:")

        row = layout.row()
        row.prop(properties, "output_directory")

        row = layout.row()
        row.prop(properties, "out_start_index")

        row = layout.row()
        row.prop(properties, "y_offset")

        row = layout.row()
        row.prop(properties, "number_of_rider_sets")

        row = layout.row()
        row.prop(properties, "number_of_recolorables")

        row = layout.row()
        row.prop(properties, "number_of_animation_frames")

        row = layout.row()
        row.prop(properties, "cast_shadows")

        row = layout.row()
        row.prop(properties, "anti_alias_with_background")

        if properties.anti_alias_with_background:
            box = layout.box()
            row = box.row()
            row.prop(properties, "maintain_aliased_silhouette")

        row = layout.row()
        row.separator()

        row = layout.row()
        row.label("Dither Palette:")

        row = layout.row()
        row.prop(properties, "palette", text="")

        if properties.palette == "CUSTOM":
            box = layout.box()
            split = box.split(.50)
            columns = [split.column(), split.column()]
            i = 0
            for color in palette_colors:
                details = palette_colors_details[color]
                columns[i % 2].row().prop(properties, "custom_palette_colors",
                                          index=i, text=details["title"])
                i += 1

        row = layout.row()
        row.label("Object Type:")

        row = layout.row()
        row.prop(properties, "render_mode", text="")

        box = layout.box()

        # Specialized properties

        if properties.render_mode == "TILES":
            self.draw_tiles_panel(scene, box)
        elif properties.render_mode == "VEHICLE":
            self.draw_vehicle_panel(scene, box)
        elif properties.render_mode == "WALLS":
            self.draw_walls_panel(scene, box)

        row = layout.row()
        row.prop(properties, "build_gx")

        if properties.build_gx:
            box = layout.box()
            box.prop(properties, "build_assetpack")

            if properties.build_assetpack:
                box2 = box.box()
                box2.prop(properties, "copy_assetpack_to_orct2")

        row = layout.row()
        row.prop(properties, "build_parkobj")

        if properties.build_parkobj:
            box = layout.box()
            box.prop(properties, "copy_parkobj_to_orct2")

    def draw_tiles_panel(self, scene, layout):
        properties = scene.rct_graphics_helper_static_properties
        general_properties = scene.rct_graphics_helper_general_properties

        row = layout.row()
        row.prop(properties, "viewing_angles")

        row = layout.row()
        row.prop(properties, "object_width")
        row.prop(properties, "object_length")

        row = layout.row()
        text = "Render"
        if general_properties.rendering:
            text = "Failed"
        row.operator("render.rct_static", text=text)

    def draw_walls_panel(self, scene, layout):
        properties = scene.rct_graphics_helper_walls_properties
        general_properties = scene.rct_graphics_helper_general_properties

        row = layout.row()
        row.prop(properties, "sloped")

        row = layout.row()
        row.prop(properties, "double_sided")

        row = layout.row()
        row.prop(properties, "doorway")

        row = layout.row()
        text = "Render"
        if general_properties.rendering:
            text = "Failed"
        row.operator("render.rct_walls", text=text)

    legacy_group_display_order = [
        "VEHICLE_SPRITE_FLAG_FLAT",
        "VEHICLE_SPRITE_FLAG_FLAT_BANKED",
        "VEHICLE_SPRITE_FLAG_GENTLE_SLOPES",
        "VEHICLE_SPRITE_FLAG_GENTLE_SLOPE_BANKED_TURNS",
        "VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPES",
        "VEHICLE_SPRITE_FLAG_DIAGONAL_SLOPE_BANKED",
        "VEHICLE_SPRITE_FLAG_STEEP_SLOPES",
        "VEHICLE_SPRITE_FLAG_VERTICAL_SLOPES",
        "VEHICLE_SPRITE_FLAG_INLINE_TWISTS",
        "VEHICLE_SPRITE_FLAG_CORKSCREWS",
        "VEHICLE_SPRITE_FLAG_ZERO_G_ROLLS",
        "VEHICLE_SPRITE_FLAG_CURVED_LIFT_HILL",
        "VEHICLE_SPRITE_FLAG_RESTRAINT_ANIMATION"
    ]

    def draw_vehicle_panel(self, scene, layout):
        properties = scene.rct_graphics_helper_vehicle_properties
        general_properties = scene.rct_graphics_helper_general_properties

        row = layout.row()
        row.prop(properties,"sprite_group_mode")

        box = layout.box()
        split = box.split(0.5)
        columns = [split.column(), split.column()]
        i = 0
        if properties.sprite_group_mode == "SIMPLE":
            for legacy_group_name in self.legacy_group_display_order:
                sprite_track_flagset = properties.legacy_spritegroups[legacy_group_name]
                index = legacy_group_names.index(legacy_group_name)
                columns[i % 2].row().prop(properties, "legacy_flags",
                                          index=index, text=sprite_track_flagset.name)
                i += 1
        else:
            columns = [column.split(0.667) for column in columns]
            subcolumns = [columns[0].column(), columns[0].column(),columns[1].column(), columns[1].column()]
            splitpoint = len(sprite_group_names) // 2
            for sprite_group_name in sprite_group_names:
                subcolumns[(i > splitpoint) * 2].row().label(sprite_group_name+":")
                subcolumns[(i > splitpoint) * 2 + 1].row().prop(properties, sprite_group_name, text = "")
                i += 1

        row = layout.row()
        row.prop(properties, "inverted_set")

        row = layout.row()
        text = "Render"
        if general_properties.rendering:
            text = "Failed"
        row.operator("render.rct_vehicle", text=text)
