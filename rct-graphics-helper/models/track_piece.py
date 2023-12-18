'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import math

from ..helpers import height_unit, normalize

def parse_direction(dir):
    dir_dict = {
        "up": (0, 0, 1),
        "down": (0, 0, -1),
        "north": (1, 0, 0),
        "east": (0, -1, 0),
        "south": (-1, 0, 0),
        "west": (0, 1, 0),
        "north_east": (1, -1, 0),
        "south_east": (-1, -1, 0),
        "south_west": (-1, 1, 0),
        "north_west": (1, 1, 0),
        "gentle_incline_up": (0, 0, 0.5),
        "gentle_incline_down": (0, 0, -0.5),
        "steep_incline_up": (0, 0, 2),
        "steep_incline_down": (0, 0, -2),
    }

    if type(dir) == str:
        directions = []
        names = dir.split(",")
        for name in names:
            if name in dir_dict:
                directions.append(dir_dict[name])
            else:
                raise Exception("Spline node field \"direction\" type \"" + dir + "\" is not a known direction")

        dx,dy,dz = 0,0,0
        for dir in directions:
            xx,yy,zz = dir
            dx,dy,dz = dx+xx,dy+yy,dz+zz

        return normalize((dx,dy,dz * height_unit))
        
    if len(dir) == 3:
        return normalize((dir[0], dir[1], dir[2] * height_unit))
    raise Exception("Spline node field \"direction\" is required and is has to be a string or an array[3]")

def parse_position(pos):
    if len(pos) == 3:
        return (pos[0], pos[1], pos[2] * height_unit)

class SplineNode:
    def __init__(self, data):
        self.position = parse_position(data["position"])
        self.direction = parse_direction(data["direction"])

        self.backward_magnitude = data.get("backward_magnitude", 1)
        self.forward_magnitude = data.get("forward_magnitude", 1)
        self.bank = data.get("bank", 0)
        self.heartline = data.get("heartline", 0)
        self.is_entry_connection = data.get("is_entry_connection", False)
        self.is_exit_connection = data.get("is_exit_connection", False)

    def get_backward_direction(self):
        x,y,z = self.direction
        return (-x * self.backward_magnitude, -y * self.backward_magnitude, -z * self.backward_magnitude)
    
    def get_forward_direction(self):
        x,y,z = self.direction
        return (x * self.forward_magnitude, y * self.forward_magnitude, z * self.forward_magnitude)
    
    def generate_previous_point(self):
        dx,dy,dz = self.get_backward_direction()
        x,y,z = self.position
        x = x + dx / self.backward_magnitude * 4
        y = y + dy / self.backward_magnitude * 4
        z = z + dz / self.backward_magnitude * 4

        ndx,ndy,ndz = self.get_forward_direction()
        return SplineNode({
            "position": [x, y, z / height_unit],
            "direction": [ndx, ndy, ndz/ height_unit],
            "bank": self.bank,
        })
    
    def generate_next_point(self):
        dx,dy,dz = self.get_forward_direction()
        x,y,z = self.position
        x = x + dx / self.forward_magnitude * 4
        y = y + dy / self.forward_magnitude * 4
        z = z + dz / self.forward_magnitude * 4
        
        ndx,ndy,ndz = self.get_forward_direction()
        return SplineNode({
            "position": [x, y, z / height_unit],
            "direction": [ndx, ndy, ndz/ height_unit],
            "bank": self.bank,
        })

class MultiTileTile:
    def __init__(self, data):
        self.tile_index = data.get("tile_index", 0)
        self.quadrants = data.get("quadrants", None)

class MultiTileFragment:
    def __init__(self, data):
        self.origin_tile_index = data.get("origin_tile_index", 0)

        self.tiles = []

        for tile_data in data.get("tiles", []):
            self.tiles.append(MultiTileTile(tile_data))

def generate_default_fragments_data(width, length):
    fragments_data = []
    for i in range(width * length):
        fragments_data.append({
            "origin_tile_index": i,
            "tiles": [
                {
                    "tile_index": i,
                    "quadrants": None,
                }
            ]
        })
    return fragments_data

class TrackPieceOrientation:
    def __init__(self, data, track_piece):
        self.view_angle = data.get("view_angle", 0)
        self.layered = data.get("layered", False)

        self.fragments = []
        
        for fragment_output in data.get("fragments", generate_default_fragments_data(track_piece.width, track_piece.length)):
            self.fragments.append(MultiTileFragment(fragment_output))

    def get_layers(self):
        if self.layered:
            return 2
        return 1


class TrackPiece:
    def __init__(self, data):
        self.id = data["id"]
        self.width = data.get("width", 1)
        self.length = data.get("length", 1)
        self.track_length = data.get("track_length", 1)

        self.spline_points = []

        for spline_point_data in data.get("spline_points", []):
            self.spline_points.append(SplineNode(spline_point_data))
            
        self.orientations = []

        for orientation_data in data.get("orientations", [
            {
                "view_angle": 0,
                "fragments": generate_default_fragments_data(self.width, self.length),
            },
            {
                "view_angle": 1,
                "fragments": generate_default_fragments_data(self.width, self.length),
            },
            {
                "view_angle": 2,
                "fragments": generate_default_fragments_data(self.width, self.length),
            },
            {
                "view_angle": 3,
                "fragments": generate_default_fragments_data(self.width, self.length),
            }
        ]):
            self.orientations.append(TrackPieceOrientation(orientation_data, self))