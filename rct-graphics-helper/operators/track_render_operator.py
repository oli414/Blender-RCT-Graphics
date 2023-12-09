'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math

from ..helpers import rotate_vec, tile_coord_to_tile_index, tile_index_to_sprite_offset, tile_index_to_tile_coord

from ..data.track_pieces import generate_track_piece_render_info, track_pieces

from ..builders.render_steps.render_step import RenderProps
from .render_operator import RCTRender

class RenderTrack(RCTRender, bpy.types.Operator):
    bl_idname = "render.rct_track"
    bl_label = "Render RCT Track"

    def create_task(self, context):
        scene = context.scene
        props = scene.rct_graphics_helper_track_properties
        general_props = scene.rct_graphics_helper_general_properties

        palette = self.palette_manager.get_base_palette(
                        general_props.palette, general_props.number_of_recolorables, "FULL")

        # Gather the general render settings so we can use them in our render steps
        render_props = RenderProps()
        render_props.from_general_props(general_props)
        render_props.aa = scene.render.use_antialiasing

        # We are going to build a render/post processing pipeline procedurally
        # using the render steps builder
        builder = self.render_steps_builder

        track_piece_infos = []

        # Gather the track piece render info, as well as collect all the track-related objects in the scene
        all_track_objs = []
        for track_piece in track_pieces:
            track_piece_render_info = generate_track_piece_render_info(context, track_piece)
            track_piece_infos.append(track_piece_render_info)
            all_track_objs += track_piece_render_info.main_objects
            for connection in track_piece_render_info.connection_objects:
                all_track_objs += connection.objects

        builder.set_visibility(all_track_objs, True)

        originally_hidden_objs = []
        originally_shown_objs = []
        for obj in all_track_objs:
            if obj.hide_render:
                originally_hidden_objs.append(obj)
            else:
                originally_shown_objs.append(obj)
        

        for track_piece_render_info in track_piece_infos:
            track_piece = track_piece_render_info.track_piece

            def get_output_index():
                get_output_index.i += 1
                return track_piece["output_indices"][get_output_index.i]
            get_output_index.i=-1


            # We expand the tiles on each side so that we can key out the connecting track pieces
            # these are genrated outside of the bounds of each track piece to ensure
            # tileability of each track piece.
            expanded_width = track_piece["width"] + 2
            expanded_length = track_piece["length"] + 2
            
            # Here we determine the order in which the tiles are output
            # as well as if tiles are combined. This order can be pre-defined
            # in the track pieces dictionary, e.g. a medium turn merges 2 tiles
            # for the middle section. But this order can also be automatically
            # generated if they follow the default multi-tile order (0, 1, 2...)
            tile_index_order = []

            if "tiles" in track_piece:
                for row in track_piece["tiles"]:
                    new_row = []
                    for current_index in row:
                        x, y = tile_index_to_tile_coord(current_index, track_piece["width"])
                        new_row.append(tile_coord_to_tile_index(x + 1, y + 1, expanded_width))
                    tile_index_order.append(new_row)
            else:
                for y in range(track_piece["length"]):
                    for x in range(track_piece["width"]):
                        new_row = [tile_coord_to_tile_index(x + 1, y + 1, expanded_width)]
                        tile_index_order.append(new_row)

            offset_x, offset_y = track_piece["offset"]
            
            for view_angle in range(track_piece["view_angles"]):
                start_view_angle = 0
                if "start_view_angle" in track_piece:
                    start_view_angle = track_piece["start_view_angle"]

                current_view_angle = view_angle + start_view_angle
                
                # Create a list of connection objects to show/hide
                show_objs = track_piece_render_info.main_objects
                hide_objs = []
                for connection in track_piece_render_info.connection_objects:
                    dx,dy,dz = (connection.direction[0], connection.direction[1], connection.direction[2])
                    dx,dy = rotate_vec(dx, dy, 4 - current_view_angle)
                    # Check if the connection faces the camera
                    if dx < 0 or dy < 0:
                        hide_objs += connection.objects
                    else:
                        show_objs += connection.objects

                disable_first_render_layer_obj=[]

                for obj in hide_objs:
                    if obj.layers[0]:
                        disable_first_render_layer_obj.append(obj)

                # Prepare the scene
                builder \
                    .move_rig((current_view_angle) * 90, offset_x, offset_y) \
                    .set_visibility(show_objs, False) \
                    .set_object_layers(disable_first_render_layer_obj, [2], [0])

                # Generate the tile index mask, the material/object index mask and the quantized render
                tile_indices = builder \
                    .render_tile_indices(render_props, expanded_width, expanded_length, offset_x, offset_y) \
                    .get_output()
                
                meta = builder \
                    .render_scene_with_meta(render_props)
                
                original_output = builder \
                    .quantize(palette,
                        meta, general_props.number_of_recolorables) \
                    .cache_output(False) \
                    .get_output()
                
                # If this track is multi-layer we need a mask
                # to seperate the foreground from the background
                multi_layer_mask = None
                if props.multi_layer:
                    multi_layer_mask = builder \
                        .reset_renderer() \
                        .set_layer("Track Occluded") \
                        .render_scene(render_props) \
                        .get_output()

                # The renderable tiles (tile index order) are extended towards the camera
                extend_multi_tile_x = 1
                extend_multi_tile_y = 1
                extend_multi_tile_dir_x = -1
                extend_multi_tile_dir_y = -1
                if current_view_angle==3 or current_view_angle==2:
                    extend_multi_tile_x = expanded_width - 2
                    extend_multi_tile_dir_x = 1
                if current_view_angle==2 or current_view_angle==1:
                    extend_multi_tile_y = expanded_length - 2
                    extend_multi_tile_dir_y = 1

                expanded_tile_index_order = []
                for order in tile_index_order:
                    new_order = []
                    for index in order:
                        new_order.append(index)
                        oy = math.floor(index / expanded_width)
                        ox = index - (oy * expanded_width)
                        x,y = ox,oy
                        if x==extend_multi_tile_x:
                            x += extend_multi_tile_dir_x
                        if y==extend_multi_tile_y:
                            y += extend_multi_tile_dir_y
                        if x != ox:
                            new_order.append((oy * expanded_width) + x)
                        if y != oy:
                            new_order.append((y * expanded_width) + ox)
                            if x != ox:
                                new_order.append((y * expanded_width) + x)
                    expanded_tile_index_order.append(new_order)

                # Seperate each tile/set of tiles using the tile index mask
                for tile_group in expanded_tile_index_order:

                    sprite_offset_x, sprite_offset_y = tile_index_to_sprite_offset(
                        tile_group[0], expanded_width, expanded_length, current_view_angle
                    )

                    tile_selection = builder \
                        .set_input(original_output) \
                        .select_tiles(tile_indices, tile_group) \
                        .get_output()
                    
                    if not props.multi_layer:
                        builder \
                            .output(get_output_index(), -sprite_offset_x, -sprite_offset_y)
                    else:
                        tile_selection = builder \
                            .cache_output(True) \
                            .get_output()

                        # Mask out the background
                        builder \
                            .set_input(tile_selection) \
                            .copy_alpha(multi_layer_mask) \
                            .output()

                        # Mask out the foreground
                        builder \
                            .set_input(tile_selection) \
                            .copy_alpha(multi_layer_mask, True) \
                            .output()
                        
                # Clean up the scene
                builder \
                    .set_visibility(show_objs, True) \
                    .set_object_layers(disable_first_render_layer_obj, [0], [2])

        # Clean the scene completely
        builder.set_visibility(originally_shown_objs, False)
        builder.set_visibility(originally_hidden_objs, False)
        builder.move_rig(0)

        # Create the list of frames with our parameters
        return builder.create_task(context)
