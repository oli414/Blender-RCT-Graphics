import json
from ..models.track_piece import TrackPiece

class TrackPieceCollection():
    def __init__(self, data):
        self.id = data["id"]

        self.track_pieces = []
        self._track_pieces_dict = {}

        for track_piece_data in data.get("track_pieces", []):
            track_piece = TrackPiece(track_piece_data)
            self.track_pieces.append(track_piece)
            self._track_pieces_dict[track_piece.id] = track_piece

    def get(self, id):
        if id in self._track_pieces_dict:
            return self._track_pieces_dict.get(id)
        print("Failed to find \"{}\" in the track piece collection \"{}\"".format(id, self.id))
        return None

class TrackPieceRepository():
    def __init__(self, paths):
        self.collections = []
        self._collections_dict = {}

        for path in paths:
            track_pieces_file = open(path)
            track_pieces_data = json.load(track_pieces_file)
            track_pieces_file.close()

            track_piece_collection = TrackPieceCollection(track_pieces_data)
            self.collections.append(track_piece_collection)
            self._collections_dict[track_piece_collection.id] = track_piece_collection

    def get(self, id):
        for collection in self.collections:
            if id.startswith(collection.id):
                return collection.get(id.replace(collection.id + ".", "", 1))
        print("Failed to find \"{}\" in the track piecee repository".format(id))
        return None