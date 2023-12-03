'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from ..models.palette import palette_colors, palette_colors_details


class GeneralProperties(bpy.types.PropertyGroup):
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)

    number_of_rider_sets = bpy.props.IntProperty(
        name="Sets of Riders",
        description="Number of unqique sets of riders. Usually the amount of peeps in the vehicle/ride divided by 2 (peeps are typically paired in groups of 2).",
        default=0,
        min=0)

    number_of_animation_frames = bpy.props.IntProperty(
        name="Animation Frames",
        description="Number of animation frames. For example in use for swinging, rotating or animated ride vehicles, animated rides, and animated scenery",
        default=1,
        min=1)

    number_of_recolorables = bpy.props.IntProperty(
        name="Recolorables",
        description="Number of recolorables on this object.",
        default=0,
        min=0,
        max=3)

    cast_shadows = bpy.props.BoolProperty(
        name="Shadows",
        description="Control whether the lights should cast shadows.",
        default=True)

    anti_alias_with_background = bpy.props.BoolProperty(
        name="Anti-Alias with Background",
        description="Causes an outline on objects. Exclusively found on RCT1 graphics.",
        default=False)

    maintain_aliased_silhouette = bpy.props.BoolProperty(
        name="Maintain Aliased Silhouette (For modular pieces)",
        description="The image is anti-aliased against the background, but is masked using the aliased silhoutte.",
        default=False)

    out_start_index = bpy.props.IntProperty(
        name="Output Starting Index",
        description="Number to start counting from for the output file names.",
        default=0,
        min=0)

    y_offset = bpy.props.IntProperty(
        name="Sprite Y Offset",
        description="Additional Y offset to add to the sprite offsets.",
        default=0)

    output_directory = bpy.props.StringProperty(
        name="Output Folder",
        description="Directory to output the sprites to.",
        maxlen=1024,
        subtype='DIR_PATH',
        default="//output")

    palette = bpy.props.EnumProperty(
        name="Palette",
        items=(
            ("AUTO", "Automatic",
             "Automatically selects the most common palette for the render type.", 1),
            ("FULL", "Default Full Color",
             "Standard palette featuring all the non-animated colors.", 2),
            ("VEHICLE", "Vehicle Gray Only",
             "Common palette for vehicles, only uses black, gray and white for non-recolorable parts.", 3),
            ("CUSTOM", "Custom",
             "Create a custom palette by selected the colors to include.", 4)
        )
    )

    defaults = []
    for color in palette_colors:
        defaults.append(palette_colors_details[color]["default"])

    custom_palette_colors = bpy.props.BoolVectorProperty(
        name="Custom Palette Colors",
        default=defaults,
        description="Which color groups to dither to. Recolorables will be excluded from this palette when used to avoid conflicts.",
        size=len(defaults))

    render_mode = bpy.props.EnumProperty(
        name="Render Mode",
        items=(
            ("TILES", "Tile(s)", "Renders an object from in-game viewing angles. Has the ability for multi-tile rendering.", 1),
            ("VEHICLE", "Vehicle",
             "Renders a vehicle from the necesssary angles given a set of track ability flags.", 2),
            ("WALLS", "Walls",
             "Renders a wall piece.", 3),
            ("TRACK", "Track",
             "Renders track pieces.", 4)
        )
    )

    rendering = bpy.props.BoolProperty(
        name="Rendering",
        description="Whether or not the RCT add-on is currently rendering.",
        default=False)

    build_gx = bpy.props.BoolProperty(
        name="Generate GX (optimized sprite file)",
        description="Whether or not to create a .dat sprite file. Having GXC installed is required.",
        default=False)

    build_assetpack = bpy.props.BoolProperty(
        name="Generate the asset pack file",
        description="Whether or not to the ORCT2 asset pack file",
        default=False)

    copy_assetpack_to_orct2 = bpy.props.BoolProperty(
        name="Copy to OpenRCT2",
        description="Copy the generated .graphics file to the ORCT2 assetpack folder.",
        default=False)

    build_parkobj = bpy.props.BoolProperty(
        name="Generate .parkobj file",
        description="Automatically build the .parkobj file. An object.json file with the object description is required in the output folder.",
        default=False)

    copy_parkobj_to_orct2 = bpy.props.BoolProperty(
        name="Copy to OpenRCT2",
        description="Copy the generated .parkobj file to the ORCT2 objects folder. Linking your OpenRCT2 Documents folder is required in the add-on preferences.",
        default=False)


def register_general_properties():
    bpy.types.Scene.rct_graphics_helper_general_properties = bpy.props.PointerProperty(
        type=GeneralProperties)


def unregister_general_properties():
    del bpy.types.Scene.rct_graphics_helper_general_properties
