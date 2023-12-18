'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import bmesh
import math
import os

from ..helpers import find_material_by_name
from ..models.track_piece import SplineNode
from ..models.track_piece_repository import TrackPieceRepository
from ..models.track_type import load_track_type

from ..res.res import res_path

north = (1, 0, 0)
east = (0, -1, 0)
south = (-1, 0, 0)
west = (0, 1, 0)
up = (0, 0, 1)

height_unit = 1/math.sqrt(6)*4

def gentle_incline(dir, factor=1):
    x,y,z=dir
    return (x,y, z + height_unit / 4 * factor)

def steep_incline(dir, factor=1):
    x,y,z=dir
    return (x,y, z + height_unit / 4 * 2 * factor)

def spline_point(coord, dir, strength=1, bank=0):
    x,y,z=coord
    dx,dy,dz=dir
    return (
        x,y,z,
        dx*strength,dy*strength,dz*strength,
        bank
    )

def set_length(dir, size):
    dx,dy,dz = dir
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    return (dx / length * size, dy / length * size, dz / length * size)

def add(v1, v2):
    x,y,z=v1
    x2,y2,z2=v2
    return (x + x2, y + y2, z + z2)
    

# Builder for populating the scene with track splines
class SplineBuilder:

    def __init__(self):
        self.prefix = ""
        self.suffix = ""
        return

    def build(self, context):
        main_track_base_objects = context.selected_objects

        track_piece_repository = TrackPieceRepository([
            os.path.join(res_path, "tracks", "rct2_track_pieces.json")
        ])
        track_type = load_track_type(
            os.path.join(res_path, "tracks", "types", "rct2", "wild_mouse_coaster.json"),
            track_piece_repository,
        )

        index = 0
        for track_piece in track_type.track_pieces:
            base_track_piece = track_piece.base_track_piece
            repeat_track_model = base_track_piece.track_length

            piece = self.create_track_piece(
                context, track_piece.id, base_track_piece.spline_points, None, main_track_base_objects,
                track_piece.scene_position, repeat_track_model
            )
        
            in_count = 1
            out_count = 1
            for spline_point in base_track_piece.spline_points:
                if spline_point.is_entry_connection:
                    in_piece = self.create_track_piece(context, "in_{}_{}".format(in_count, track_piece.id), [
                        spline_point.generate_previous_point(),
                        spline_point
                    ], piece, main_track_base_objects, track_piece.scene_position, 1, True, True)
                    in_count += 1
                if spline_point.is_exit_connection:
                    out_piece = self.create_track_piece(context, "out_{}_{}".format(out_count, track_piece.id), [
                        spline_point,
                        spline_point.generate_next_point()
                    ], piece, main_track_base_objects, track_piece.scene_position, 1, True, True)
                    out_count += 1


            index += 1

    def create_track_piece(self, context, name, points, parent, base_objects, offset, repeat=1, hide=False, mask=False):
        spline_object = self.create_spline(context, name, points, offset)
        spline_object.hide = hide
        spline_object.parent = parent
        context.scene.objects.link(spline_object)

        generated_objects = []
        for obj in base_objects:
            target_obj_name = obj.name + "_obj_" + name

            pre_existing = self.get_scene_object(context, target_obj_name)
            if pre_existing is not None:
                generated_objects.append(pre_existing)
                continue

            target_obj = obj.copy()
            target_obj.name = target_obj_name
            target_obj.animation_data_clear()
            context.scene.objects.link(target_obj)

            target_obj.parent = spline_object
            generated_objects.append(target_obj)

            for i in range(20):
                target_obj.layers[i] = obj.layers[i]
                
            if not target_obj.layers[0]:
                target_obj.hide = True
            else:
                target_obj.hide = hide

            target_obj.hide_render = hide
        
        for obj in generated_objects:
            obj.parent = spline_object
            
            array_modifier = None
            if "Track Repeat" in obj.modifiers:
                array_modifier = obj.modifiers["Track Repeat"]
            else:
                array_modifier = obj.modifiers.new("Track Repeat", 'ARRAY')
                array_modifier.fit_type = "FIXED_COUNT"
                array_modifier.count = repeat

            array_modifier.curve = spline_object

            curve_modifier = None
            if "Track Curve" in obj.modifiers:
                curve_modifier = obj.modifiers["Track Curve"]
            else:
                curve_modifier = obj.modifiers.new("Track Curve", 'CURVE')
            
            curve_modifier.object = spline_object

        return spline_object

    def create_spline(self, context, name, points, offset):
        name = self.prefix + name + self.suffix
        if name in bpy.data.curves:
            bpy.data.curves.remove(bpy.data.curves[name])

        curve_data = bpy.data.curves.new(name, type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.use_stretch = True
        curve_data.use_deform_bounds = True
        curve_data.twist_mode = "Z_UP"

        bezier = curve_data.splines.new('BEZIER')
        bezier.bezier_points.add(len(points) - 1)
        for i, coord in enumerate(points):
            p = coord.position
            x,y,z=p
            ox,oy,oz = offset
            x += ox
            y += oy
            z += oz
            ndx,ndy,ndz=coord.get_backward_direction()
            pdx,pdy,pdz=coord.get_forward_direction()
            bezier.bezier_points[i].co = (x,y,z)
            bezier.bezier_points[i].handle_left_type  = 'FREE'
            bezier.bezier_points[i].handle_right_type = 'FREE'
            bezier.bezier_points[i].handle_left = (x + ndx, y + ndy, z + ndz)
            bezier.bezier_points[i].handle_right  = (x + pdx, y + pdy, z + pdz)
            bezier.bezier_points[i].tilt = coord.bank / 57.29577951308232

        curve_object = self.create_scene_object(
            context, name, curve_data)
            
        return curve_object

    def create_scene_object(self, context, name, data=None):
        name = self.prefix + name + self.suffix
        if name in context.scene.objects:
            bpy.data.objects.remove(
                context.scene.objects[name], do_unlink=True)
        return bpy.data.objects.new(name, data)

    def remove_scene_object(self, context, name):
        if name in context.scene.objects:
            bpy.data.objects.remove(
                context.scene.objects[name], do_unlink=True)

    def get_scene_object(self, context, name):
        if name in context.scene.objects:
            return context.scene.objects[name]
        return None
