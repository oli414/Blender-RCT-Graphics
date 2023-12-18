import json

def parse_offset(pos):
    if len(pos) == 3:
        return (pos[0], pos[1], pos[2] * 8)

class TrackPiece():
    def __init__(self, data, track_piece_repository):
        self.id = data["id"]
        self.output_indices = data.get("output_indices", None)
        self.animation_frames = data.get("animation_frames", 1)

        scene_pos_data = data.get("scene_position", [0, 0, 0])
        self.scene_position = (scene_pos_data[0], scene_pos_data[1], scene_pos_data[2])

        base_track_piece_id = data["base_track_piece"]
        self.base_track_piece = track_piece_repository.get(base_track_piece_id)
        
        self.limit_orientations = data.get("limit_orientations", len(self.base_track_piece.orientations))

        self.fragment_offsets = []

        for fragment_offset_data in data.get("fragment_offsets", []):
            self.fragment_offsets.append(parse_offset(fragment_offset_data))

class TrackType():
    def __init__(self, data, track_piece_repository):
        self.id = data["id"]
        self.name = data["name"]

        # Each track piece spline point can specify a heartline offset,
        # with this multiplier it can be scaled.
        self.heartline_multiplier = data.get("heartline_multiplier", 1)

        # The base height is the height from which the track is rotated from for
        # a normal banked turn. Typically this is the height at which the vehicle wheels
        # touch the track.
        self.base_height = data.get("base_height", 0)

        self.track_pieces = []
        for track_piece_data in data.get("track_pieces", []):
            self.track_pieces.append(TrackPiece(track_piece_data, track_piece_repository))

def load_track_type(path, track_piece_repository):
    file = open(path)
    data = json.load(file)
    file.close()
    return TrackType(data, track_piece_repository)