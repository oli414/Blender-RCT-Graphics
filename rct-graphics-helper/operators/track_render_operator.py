'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from ..models.track_piece_repository import TrackPieceRepository
from ..models.track_type import load_track_type

from ..renderer import RenderSettings

from ..res.res import res_path

from ..helpers import rotate_vec, tile_coord_to_tile_index, tile_index_to_sprite_offset, tile_index_to_tile_coord

from ..data.track_pieces import generate_track_piece_render_info

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

        render_settings = RenderSettings()
        render_settings.from_general_props(general_props)
        render_settings.aa = scene.render.use_antialiasing
        render_settings.layer = "Track"

        # We are going to build a render/post processing pipeline procedurally
        # using the render steps builder
        builder = self.render_steps_builder

        track_piece_repository = TrackPieceRepository([
            os.path.join(res_path, "tracks", "rct2_track_pieces.json")
        ])
        track_type = load_track_type(
            os.path.join(res_path, "tracks", "types", "rct2", "wild_mouse_coaster.json"),
            track_piece_repository,
        )

        track_piece_infos = []

        # Gather the track piece render info, as well as collect all the track-related objects in the scene
        all_track_objs = []
        for track_piece in track_type.track_pieces:
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

            floor = -100

            def get_output_index():
                get_output_index.i += 1
                return track_piece.output_indices[get_output_index.i]
            get_output_index.i=-1

            offset_x, offset_y, offset_z = track_piece.scene_position

            for animation_frame_index in range(track_piece.animation_frames):

                orientation_renders = []
                # Prepare the renders
                for orientation_i in range(len(track_piece.base_track_piece.orientations)):
                    if orientation_i >= track_piece.limit_orientations:
                        continue

                    orientation = track_piece.base_track_piece.orientations[orientation_i]

                    current_view_angle = orientation.view_angle

                    # Create a list of connection objects to show/hide
                    show_main_objs = track_piece_render_info.main_objects
                    show_objs = []
                    hide_objs = []
                    for connection in track_piece_render_info.connection_objects:
                        dx,dy,dz = (connection.direction[0], connection.direction[1], connection.direction[2])
                        dx,dy = rotate_vec(dx, dy, 4 - current_view_angle)

                        print(track_piece.id)
                        print("{} {} {}".format(dx, dy, dz))

                        if dx == 0 and dy == 0 and dz < 0:
                            floor = connection.position[2]
                        # Check if the connection faces the camera
                        if dx < 0 or dy < 0 or (dx == 0 and dy == 0 and dz > 0):
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
                        .set_animation_frame(animation_frame_index) \
                        .set_visibility(show_main_objs, False) \
                        .set_visibility(show_objs, True) \
                        .set_object_layers(disable_first_render_layer_obj, [2], [0])

                    # Generate the tile index mask, the material/object index mask and the quantized render
                    tile_indices = builder \
                        .render_tile_indices(render_props, track_piece.base_track_piece.width, track_piece.base_track_piece.length, offset_x, offset_y, floor) \
                        .get_output()
                    
                    meta = builder \
                        .render_scene_with_meta(render_props)
                    
                    render = builder.get_output()

                    expanded_meta = builder \
                        .set_visibility(show_objs, False) \
                        .render_scene_with_meta(render_props) \
                        
                    expanded_render = builder.get_output()

                    original_output = builder \
                        .set_input(expanded_render) \
                        .copy_alpha(render) \
                        .cache_output(False) \
                        .quantize(palette, meta, general_props.number_of_recolorables) \
                        .cache_output(False) \
                        .get_output()
                    
                    # If this track is multi-layer we need a mask
                    # to seperate the foreground from the background
                    multi_layer_mask = None
                    if orientation.layered:
                        multi_layer_mask = builder \
                            .reset_renderer() \
                            .set_layer("Track Occluded") \
                            .render_scene(render_props) \
                            .get_output()
                
                    # Clean up the scene
                    builder \
                        .set_animation_frame(0) \
                        .set_visibility(show_objs + show_main_objs, True) \
                        .set_object_layers(disable_first_render_layer_obj, [0], [2])

                    orientation_renders.append((original_output, tile_indices, multi_layer_mask))

                for layer in range(2):
                    for orientation_i in range(len(track_piece.base_track_piece.orientations)):
                        if orientation_i >= track_piece.limit_orientations:
                            continue

                        orientation = track_piece.base_track_piece.orientations[orientation_i]

                        if layer==1 and not orientation.layered:
                            continue

                        original_output, tile_indices, multi_layer_mask = orientation_renders[orientation_i]
                        current_view_angle = orientation.view_angle
                        
                        # Seperate each tile/set of tiles using the tile index mask
                        fragment_index = 0
                        for fragment in orientation.fragments:
                            sprite_offset_x, sprite_offset_y = tile_index_to_sprite_offset(
                                fragment.tiles[0].tile_index, track_piece.base_track_piece.width, track_piece.base_track_piece.length, current_view_angle
                            )

                            if len(track_piece.fragment_offsets) > 0:
                                fx, fy, fz = track_piece.fragment_offsets[fragment_index]

                                if current_view_angle == 0 or current_view_angle == 2:
                                    fx = -fx
                                else:
                                    fy = -fy

                                sprite_offset_x -= fx + fy
                                sprite_offset_y += abs(fx + fy) / 2 + fz
                            
                            builder \
                                .set_input(original_output) \
                                .select_tiles(tile_indices, fragment.tiles)
                            
                            if not orientation.layered:
                                builder \
                                    .output(get_output_index(), -sprite_offset_x, -sprite_offset_y)
                            else:
                                if layer==0:
                                    # Mask out the foreground
                                    builder \
                                        .copy_alpha(multi_layer_mask, True) \
                                        .output(get_output_index(), -sprite_offset_x, -sprite_offset_y)

                                if layer==1:
                                    # Mask out the background
                                    builder \
                                        .copy_alpha(multi_layer_mask) \
                                        .output(get_output_index(), -sprite_offset_x, -sprite_offset_y)
                                    
                            fragment_index += 1

        # Clean the scene completely
        builder.set_visibility(originally_shown_objs, False)
        builder.set_visibility(originally_hidden_objs, False)
        builder.move_rig(0)

        # Create the list of frames with our parameters
        return builder.create_task(context)
