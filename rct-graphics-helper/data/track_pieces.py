import math

north = (1, 0, 0)
east = (0, -1, 0)
south = (-1, 0, 0)
west = (0, 1, 0)

up = (0, 0, 1)
down = (0, 0, -1)

height_unit = 1/math.sqrt(6)*2

def normalize(dir):
    dx,dy,dz = dir
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    return (dx / length, dy / length, dz / length)

north_east = normalize((1, -1, 0))
south_east = normalize((-1, -1, 0))
south_west = normalize((-1, 1, 0))
noth_west = normalize((1, 1, 0))

def gentle_incline(dir, pos=1):
    dx,dy,dz = dir
    return normalize((dx,dy,dz + (height_unit / 2) * pos))

def steep_incline(dir, pos=1):
    dx,dy,dz = dir
    return normalize((dx,dy,dz + (height_unit) * pos))

def track_point(pos, dir, bank=0, plength=1, nlength=1):
    dx,dy,dz = dir
    return (pos, (dx * -nlength, dy * -nlength, dz * -nlength), (dx * plength, dy * plength, dz * plength), bank)

track_pieces = [
    {
        "name": "straight",
        "points": [
            track_point((-2, 0, 0), north),
            track_point((2, 0, 0), north)
        ],
        "offset": (0, -8),
        "width": 1,
        "length": 1,
        "start_view_angle": 0,
        "view_angles": 2,
        "output_indices": [
            16900, 16901
        ]
    },
    {
        "name": "gentle_incline",
        "points": [
            track_point((-2, 0, 0), gentle_incline(north)),
            track_point((2, 0, height_unit * 2), gentle_incline(north))
        ],
        "offset": (16, 0),
        "width": 1,
        "length": 1,
        "start_view_angle": 0,
        "view_angles": 4,
        "output_indices": [
            16922, 16923, 16924, 16925
        ]
    },
    {
        "name": "flat_to_gentle_incline_up",
        "points": [
            track_point((-2, 0, 0), north, 0, 1.5, 1.5),
            track_point((2, 0, height_unit), gentle_incline(north), 0, 1.5, 1.5)
        ],
        "offset": (16, -8),
        "width": 1,
        "length": 1,
        "start_view_angle": 0,
        "view_angles": 4,
        "output_indices": [
            16914, 16915, 16916, 16917
        ]
    },
    {
        "name": "flat_to_gentle_incline_down",
        "points": [
            track_point((-2, 0, 0), gentle_incline(north), 0, 1.5, 1.5),
            track_point((2, 0, height_unit), north, 0, 1.5, 1.5)
        ],
        "offset": (16, -16),
        "width": 1,
        "length": 1,
        "start_view_angle": 0,
        "view_angles": 4,
        "output_indices": [
            16918, 16919, 16920, 16921
        ]
    },
    {
        "name": "small_turn",
        "points": [
            track_point((-2, 0, 0), north, 0, 1.1, 1.1),
            track_point((0, 2, 0), west, 0, 1.1, 1.1)
        ],
        "offset": (0, -16),
        "width": 1,
        "length": 1,
        "view_angles": 4,
        "output_indices": [
            16994, 16995, 16996, 16997 #28805, 28806, 28807, 28808
        ]
    },
    {
        "name": "medium_turn",
        "points": [
            track_point((-4, 2, 0), north, 0, 3.5, 3.5),
            track_point((2, -4, 0), east, 0, 3.5, 3.5)
        ],
        "offset": (0, -26),
        "width": 2,
        "length": 2,
        "tiles": [
            [1], [3, 0], [2]
        ],
        "view_angles": 4,
        "output_indices": [
            16998, 16999, 17000,
            17001, 17002, 17003,
            17004, 17005, 17006,
            17007, 17008, 17009,
        ],
        "repeat_track_model": 2
    },
    #{
    #    "name": "large_turn",
    #    "points": [
    #        track_point((-6, 4, 0), north, 0, 5.5, 5.5),
    #        track_point((4, -6, 0), east, 0, 5.5, 5.5)
    #    ],
    #    "offset": (0, -40),
    #    "width": 3,
    #    "length": 3,
    #    "tiles": [
    #        [2, 1], [5], [4, 8], [7], [6, 3]
    #    ],
    #    "start_view_angle": 0,
    #    "view_angles": 4
    #},
    #{
    #    "name": "diagonal",
    #    "points": [
    #        track_point((-2, 2, 0), north_east),
    #        track_point((2, -2, 0), north_east)
    #    ],
    #    "offset": (0, -52),
    #    "width": 3,
    #    "length": 3,
    #    "tiles": [
    #        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    #    ],
    #    "start_view_angle": 0,
    #    "view_angles": 2
    #},
    #"straight_gentle_incline": {
    #    "points": [
    #        track_point((-2, 0, 0), gentle_incline(north)),
    #        track_point((2, 0, height_unit), gentle_incline(north))
    #    ],
    #    "start_view_angle": 0,
    #    "view_angles": 4
    #},
]

class TrackPieceRenderInfo:
    def __init__(self, track_piece, main_objects, connection_objects):
        self.track_piece = track_piece
        self.main_objects = main_objects
        self.connection_objects = connection_objects

class TrackInfoRenderInfo:
    def __init__(self, width, length, track_point, backwards, objects):
        self.objects = objects

        pos,ndir,pdir,bank = track_point
        width += 2
        length += 2

        dir = pdir
        if backwards:
            dir = ndir

        x,y,z = pos
        dx,dy,dz = normalize(dir)

        x = math.floor((x+dx) / 4 + width / 2)
        y = math.floor((y+dy) / 4 + length / 2)

        self.tile_index = (y * width) + x

        self.direction = [0, 0, 1]
        if z < 0:
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

        

def find_objects(context, name):
    needle = "_obj_{}".format(name)
    found = []
    for obj in context.scene.objects:
        if obj.name.endswith(needle):
            found.append(obj)
    return found

def generate_track_piece_render_info(context, track_piece):
    track_name = track_piece["name"]
    main_objects = find_objects(context, track_name)
    in_objects = find_objects(context, "in_{}".format(track_name))
    out_objects = find_objects(context, "out_{}".format(track_name))
    track_piece_info = TrackPieceRenderInfo(track_piece, main_objects, [
        TrackInfoRenderInfo(
            track_piece["width"], track_piece["length"],
            track_piece["points"][0],
            True,
            in_objects),
        TrackInfoRenderInfo(
            track_piece["width"], track_piece["length"],
            track_piece["points"][len(track_piece["points"]) - 1],
            False,
            out_objects)
    ])
    return track_piece_info
