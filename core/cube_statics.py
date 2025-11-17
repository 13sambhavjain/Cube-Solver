# standard library imports
from functools import cache
from collections.abc import Callable
import random
# core imports
from .colors import Color, Colors
from .directions import SideDirections, Direction
from .moves import Moves, Move
from .face import Face, FaceId
from .shortnames import *

class CubeStatics():
    # colors = [w,r,g,y,o,b]
    # sturcture =   # w
                    # b o
                    # y g
                        # r
    def __getitem__(self, index: FaceId) -> Face: ... #type: ignore
    faceIds = Colors()
    colors = Colors() # [w, b, r, g, y, o] -  with some cyclic Functionalities
    side_directions = SideDirections() # [up, right, down, left] - with some cyclic Functionalities
    direction2faceId: dict[FaceId, dict[Direction, FaceId]] = { # mapping SideDirection to Face center color
        w: {right:o, down:b, left:r, up:g, back:y},
        y: {right:g, down:r, left:b, up:o, back:w},
        r: {right:w, down:b, left:y, up:g, back:o},
        o: {right:g, down:y, left:b, up:w, back:r},
        b: {right:o, down:y, left:r, up:w, back:g},
        g: {right:w, down:r, left:y, up:o, back:b}
    }
    faceId2direction: dict[FaceId, dict[FaceId, Direction]] = { # mapping Face center color to SideDirection
        w: {o:right, b:down, r:left, g:up, y:back},
        y: {g:right, r:down, b:left, o:up, w:back},
        r: {w:right, b:down, y:left, g:up, o:back},
        o: {g:right, y:down, b:left, w:up, r:back},
        b: {o:right, y:down, r:left, w:up, g:back},
        g: {w:right, r:down, y:left, o:up, b:back}
    }
    movementDirection2index: dict[Direction, tuple[str, int]] = { # mapping movement of SideDirection to row/column index
        up: ('x', 0),
        down: ('x', -1),
        right: ('y', -1),
        left: ('y', 0)
    }

    @staticmethod
    def faceId2color(faceid: FaceId) -> Color:
        return faceid
    
    @staticmethod
    def color2faceId(color: Color) -> FaceId:
        return color
    
    @staticmethod
    def formula2Moves(front: FaceId, top: FaceId, formula: str) -> Moves:
        moves = Moves()
        rotate = CubeStatics.side_directions.index(CubeStatics.faceId2direction[front][top])
        direction_map: dict[str, FaceId] = {
            'U': CubeStatics.direction2faceId[front][CubeStatics.side_directions[rotate]],
            'R': CubeStatics.direction2faceId[front][CubeStatics.side_directions[(rotate+1)%4]],
            'D': CubeStatics.direction2faceId[front][CubeStatics.side_directions[(rotate+2)%4]],
            'L': CubeStatics.direction2faceId[front][CubeStatics.side_directions[(rotate+3)%4]],
            'B': CubeStatics.direction2faceId[front][back],
            'F': front
        }
        i = 0
        n = len(formula) - 1
        while i < n:
            if formula[i+1] in ['`', "'"]:
                moves.append(Move(direction_map[formula[i]], -1))
                i += 2
            elif formula[i+1] in ['2', '\u00b2']:
                moves.append(Move(direction_map[formula[i]], 2))
                i += 2
            else:
                moves.append(Move(direction_map[formula[i]]))
                i += 1
        if i == n:
            moves.append(Move(direction_map[formula[i]]))

        return moves
    
    @classmethod
    @cache
    def get_neighbors(cls, face_id: FaceId) -> list[tuple[FaceId, Direction]]:
        """Return 4 neighboring faces of `face_id` in order: right, up, left, down."""
        return [
            (cls.direction2faceId[face_id][right],  cls.faceId2direction[cls.direction2faceId[face_id][right]][face_id]),
            (cls.direction2faceId[face_id][up],     cls.faceId2direction[cls.direction2faceId[face_id][up]][face_id]),
            (cls.direction2faceId[face_id][left],   cls.faceId2direction[cls.direction2faceId[face_id][left]][face_id]),
            (cls.direction2faceId[face_id][down],   cls.faceId2direction[cls.direction2faceId[face_id][down]][face_id]),
        ]

    @staticmethod
    def getSolvedState(size:int = 3, faceId2fillColor: Callable[[FaceId], Color] = lambda x: x)  -> dict[FaceId, Face]:
        """Return the solved state of a Cube of given size."""
        return {
            faceId: Face(size, faceId2fillColor(faceId))
            for faceId in CubeStatics.faceIds
        }
    
    @staticmethod
    def get_randomScramble(limit: int = 20) -> Moves:
        moves: Moves = Moves()
        for _ in range(limit):
            moves.append(Move(faceId=random.choice(CubeStatics.faceIds), turns=random.choice([1,2,3])))
        return moves