'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
from ..data.track_pieces import track_pieces

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

        index = 0
        for track_piece in track_pieces:
            repeat_track_model = 1
            if "repeat_track_model" in track_piece:
                repeat_track_model = track_piece["repeat_track_model"]

            piece = self.create_track_piece(context, track_piece["name"], track_piece["points"], main_track_base_objects, track_piece["offset"], repeat_track_model)
        
            first_point = track_piece["points"][0]
            last_point = track_piece["points"][len(track_piece["points"]) - 1]

            p, nd, pd, bank = first_point
            p = add(p, set_length(nd, 4))
            nd = set_length(nd, 1)
            pd = set_length(pd, 1)
            in_piece = self.create_track_piece(context, "in_" + track_piece["name"], [
                (p, nd, pd, bank),
                first_point
            ], main_track_base_objects, track_piece["offset"], 1, True)

            p, nd, pd, bank = last_point
            p = add(p, set_length(pd, 4))
            nd = set_length(nd, 1)
            pd = set_length(pd, 1)
            out_piece = self.create_track_piece(context, "out_" + track_piece["name"], [
                last_point,
                (p, nd, pd, bank)
            ], main_track_base_objects, track_piece["offset"], 1, True)

            index += 1

    def create_track_piece(self, context, name, points, base_objects, offset, repeat=1, hide=False):
        spline_object = self.create_spline(context, name, points, offset)
        spline_object.hide = hide
        context.scene.objects.link(spline_object)

        for obj in base_objects:
            target_obj_name = obj.name + "_obj_" + name
            self.remove_scene_object(context, target_obj_name)
            target_obj = obj.copy()
            target_obj.name = target_obj_name
            target_obj.animation_data_clear()
            context.scene.objects.link(target_obj)

            for i in range(20):
                target_obj.layers[i] = obj.layers[i]
            target_obj.hide = hide
            target_obj.hide_render = hide

            if "Track Repeat" in target_obj.modifiers:
                target_obj.modifiers.remove(target_obj.modifiers["Track Repeat"])
            array_modifier = target_obj.modifiers.new("Track Repeat", 'ARRAY')
            
            array_modifier.fit_type = "FIXED_COUNT"
            array_modifier.count = repeat
            array_modifier.curve = spline_object

            if "Track Curve" in target_obj.modifiers:
                target_obj.modifiers.remove(target_obj.modifiers["Track Curve"])
            curve_modifier = target_obj.modifiers.new("Track Curve", 'CURVE')
            curve_modifier.object = spline_object
        
        return spline_object

    def create_spline(self, context, name, points, offset):
        name = self.prefix + "Track_Spline_" + name + self.suffix
        if name in bpy.data.curves:
            bpy.data.curves.remove(bpy.data.curves[name])

        curve_data = bpy.data.curves.new(name, type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.use_stretch = True
        curve_data.use_deform_bounds = True

        bezier = curve_data.splines.new('BEZIER')
        bezier.bezier_points.add(len(points) - 1)
        for i, coord in enumerate(points):
            p,nd,pd,bank = coord
            x,y,z=p
            ox,oy = offset
            x += ox
            y += oy
            ndx,ndy,ndz=nd
            pdx,pdy,pdz=pd
            bezier.bezier_points[i].co = (x,y,z)
            bezier.bezier_points[i].handle_left_type  = 'FREE'
            bezier.bezier_points[i].handle_right_type = 'FREE'
            bezier.bezier_points[i].handle_left = (x + ndx, y + ndy, z + ndz)
            bezier.bezier_points[i].handle_right  = (x + pdx, y + pdy, z + pdz)
            bezier.bezier_points[i].tilt = bank / 57.29577951308232

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
