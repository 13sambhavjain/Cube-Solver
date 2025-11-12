#standard lib imports
from functools import cache
# core imports
from .coordinates import Position, Coords
from .cube_statics import CubeStatics
from .directions import Direction
from .shortnames import *

class Cube3x3Statics(CubeStatics):
    sideDirection2edgePosition: dict[Direction, Position] = { # Coordinate of edges in a face grid of 3x3 Cube
        up: Position(0,1),
        down: Position(2, 1),
        right: Position(1, 2),
        left: Position(1, 0)
    }
    cornerCoord: list[Position] = [
        Position(0, 0), Position(0, 2), Position(2, 2), Position(2, 0)
    ]

    @staticmethod
    def BackEdgePosition(position: Position) -> Position:
        """Given edge coordinates (i, j)(front), return the opposite(back) edge coordinates."""
        # implement edge check
        i, j = position
        if (i+j) == 3:
            return Position(i-1, j-1)
        else: #if edge then i+j == 1
            return Position(i+1, j+1)

    @staticmethod
    def cornerAfterRotation(coords, rotatingFace, check=True):
        raise NotImplementedError
        if check:
            other1, other2 = Cube.CotherSide(*coords)
            if rotatingFace not in (other1[0], other2[0]):
                return coords
        c,i,j = coords
        newFace = Cube.direction2color[rotatingFace][Cube.directions[Cube.directions.index(Cube.color2direction[rotatingFace][c]) - 3]]
        increment = (Cube.directions.index(Cube.color2direction[c][newFace]) - Cube.directions.index(Cube.color2direction[newFace][c]))%4
        if increment == 2:
            return newFace, i, j
        else:
            return newFace, *Cube.cornerCoord[(Cube.cornerCoord.index((i,j)) + increment)%4]

    @staticmethod
    def EdgeOtherSide(coords: Coords) -> Coords:
        """Given coords of one side of an edge piece, 
        return the coords of the other side of that edge piece."""      
        face_id, i, j = coords
        ind = int(CubeStatics.colors.index(face_id))
        k = (3 - (i + j))//2
        if (i + j)&1:
            # edges
            return Coords(CubeStatics.colors[(ind + 1 + k*3 + ((ind + (i&1))&1))%6], k + (ind&1), k + ((ind + 1)&1))
        else:
            raise ValueError
    
    @cache
    @staticmethod
    def CotherSide(corner_coords: Coords):
        # raise NotImplementedError
        # corner
        cornerColors = [
            {Coords(w, 0, 0), Coords(g, 2, 2), Coords(r, 0, 2)},
            {Coords(w, 0, 2), Coords(o, 0, 2), Coords(g, 0, 2)},
            {Coords(w, 2, 0), Coords(b, 0, 0), Coords(r, 2, 2)},
            {Coords(w, 2, 2), Coords(b, 0, 2), Coords(o, 0, 0)},
            {Coords(y, 0, 0), Coords(b, 2, 2), Coords(o, 2, 0)},
            {Coords(y, 0, 2), Coords(o, 2, 2), Coords(g, 0, 0)},
            {Coords(y, 2, 0), Coords(b, 2, 0), Coords(r, 2, 0)},
            {Coords(y, 2, 2), Coords(g, 2, 0), Coords(r, 0, 0)}
        ]
        for colors in cornerColors:
            if corner_coords in colors:
                return colors - {corner_coords}
        else:
            raise ValueError(f'Given coords are not of a corner {corner_coords!r}')

