import math
import os
import json

import sys
sys.setrecursionlimit(5000)

from ..models.track_piece import TrackPiece

from ..res.res import res_path

from ..helpers import height_unit, normalize

class TrackPieceRenderInfo:
    def __init__(self, track_piece, main_objects, connection_objects):
        self.track_piece = track_piece
        self.main_objects = main_objects
        self.connection_objects = connection_objects

class TrackInfoRenderInfo:
    def __init__(self, width, length, position, direction, objects):
        self.objects = objects

        width += 2
        length += 2

        print("track render info (pos) (dir)")
        print(position)
        print(direction)

        x,y,z = position
        dx,dy,dz = normalize(direction)

        self.position = [x,y,z]
        
        print("{} {}".format(math.floor(x / 4), math.floor(y / 4)))
        print("{} {}".format(dx, dy))

        x = math.floor((x+dx) / 4 + width / 2)
        y = math.floor((y+dy) / 4 + length / 2)
        
        print("{} {}".format(x, y))

        self.tile_index = (y * width) + x

        self.direction = [0, 0, 0]
        if dz > 0:
            self.direction = [0, 0, 1]
        if dz < 0:
            self.direction = [0, 0, -1]

        if x == 0:
            self.direction[0] = -1
            self.direction[2] = 0
        if y == 0:
            self.direction[1] = -1
            self.direction[2] = 0
        if x == width - 1:
            self.direction[0] = 1
            self.direction[2] = 0
        if y == length - 1:
            self.direction[1] = 1
            self.direction[2] = 0



def load_track_pieces(path=os.path.join(res_path, "tracks", "track_pieces.json")):
    track_pieces_file = open(path)
    
    track_pieces_data = json.load(track_pieces_file)

    track_pieces_file.close()
    
    track_pieces = []
    for track_piece_data in track_pieces_data:
        track_pieces.append(TrackPiece(track_piece_data))

    return track_pieces


def find_objects(context, name):
    needle = "_obj_{}".format(name)
    found = []
    for obj in context.scene.objects:
        if obj.name.endswith(needle):
            found.append(obj)
    return found

def generate_track_piece_render_info(context, track_piece):
    base_track_piece = track_piece.base_track_piece
    track_name = track_piece.id
    main_objects = find_objects(context, track_name)

    connections = []

    in_count = 1
    out_count = 1
    for spline_point in base_track_piece.spline_points:
        if spline_point.is_entry_connection:
            in_objects = find_objects(context, "in_{}_{}".format(in_count, track_name))
            connections.append(TrackInfoRenderInfo(
                base_track_piece.width,
                base_track_piece.length,
                spline_point.position,
                spline_point.get_backward_direction(),
                in_objects)
            )
            in_count += 1
        if spline_point.is_exit_connection:
            out_objects = find_objects(context, "out_{}_{}".format(out_count, track_name))
            connections.append(TrackInfoRenderInfo(
                base_track_piece.width,
                base_track_piece.length,
                spline_point.position,
                spline_point.get_forward_direction(),
                out_objects)
            )
            out_count += 1

    track_piece_info = TrackPieceRenderInfo(track_piece, main_objects, connections)
    return track_piece_info
