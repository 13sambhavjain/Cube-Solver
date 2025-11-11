# from typing import TYPE_CHECKING, TypeVar
# if TYPE_CHECKING:
#     from CubeClass import Cube
# Create a TypeVar that refers to subclasses of CubeMovements
# _TCube = TypeVar("_TCube", bound="CubeMovements")
from face import FaceId, Face
from moves import Move, Moves
from cube_statics import CubeStatics
from shortnames import *


class CubeMovements(CubeStatics):
    """
    Mixin class providing movement and rotation methods for Cube.
    Requires the implementing class to support __getitem__, __setitem__,
    and get_neighbors().
    """
    def apply_formula(self, front: FaceId = w, top: FaceId = w, *formulas: str) -> Moves:
        moves = Moves()
        for formula in formulas:
            current_moves = CubeStatics.formula2Moves(front, top, formula)
            moves.extend(current_moves)
        return self.apply_moves(moves)
    
    def apply_scramble(self, sequence: str) -> Moves:
        return self.apply_formula(g, w, sequence)

    def apply_moves(self, moves: Moves) -> Moves:
        moves.make_efficient()
        for move in moves:
            self.make_move(move)
        return moves

    def clockwise(self, face_id: FaceId):
        self[face_id].rotate_clockwise()
        neighbors = self.get_neighbors(face_id)
        edges = [self[f].get_edge(d) for f, d in neighbors]
        
        for (f, d), new_edge in zip(neighbors, edges[1:] + edges[:1]): # change here for opposite rotation
            self[f].set_edge(d, new_edge)
        return Move(face_id)
    
    def anticlockwise(self, face_id: FaceId):
        self[face_id].rotate_anticlockwise()
        neighbors = self.get_neighbors(face_id)
        edges = [self[f].get_edge(d) for f, d in neighbors]
        
        for (f, d), new_edge in zip(neighbors, edges[-1:] + edges[:-1]): # change here for opposite rotation
            self[f].set_edge(d, new_edge)
        return Move(face_id, -1)
    
    def double_rotate(self, face_id: FaceId):
        self[face_id].rotate_180()
        neighbors = self.get_neighbors(face_id)
        edges = [self[f].get_edge(d) for f, d in neighbors]
        
        for (f, d), new_edge in zip(neighbors, edges[2:] + edges[:2]):  # 180° rotation
            self[f].set_edge(d, new_edge[::-1])  # reverse edge orientation
        return Move(face_id, 2)
    
    def make_move(self, move: Move):
        if move.turns == 0:
            return move
        if move.turns == 1:
            return self.clockwise(move.faceId)
        elif move.turns == 2:
            return self.double_rotate(move.faceId)
        elif move.turns == 3:
            return self.anticlockwise(move.faceId)
        else:
            raise ValueError(f"Invalid number of turns in move: {move}")
    
    def apply_randomScramble(self, limit: int = 20) -> Moves:
        moves = self.get_randomScramble(limit)
        return self.apply_moves(moves)
    

    