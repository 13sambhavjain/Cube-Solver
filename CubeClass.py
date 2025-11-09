from copy import copy, deepcopy
import random
from Colors import Colors, Color
from Face import Face, FaceId, FaceIds, Position, Coords
from Directions import SideDirections, Direction
from Moves import Move
from old_Colors import *
from collections.abc import Callable
from functools import cache
class CubeStructure():
    # colors = [w,r,g,y,o,b]
    # sturcture =   # w
                    # b o
                    # y g
                        # r

    faceIds = Colors()
    colors = Colors() # [w, b, r, g, y, o] -  with some cyclic Functionalities
    directions = SideDirections() # [up, right, down, left] - with some cyclic Functionalities
    direction2faceId: dict[FaceId, dict[Direction, FaceId]] = { # mapping SideDirection to Face center color
        w: {right:o, down:b, left:r, up:g, opp:y},
        y: {right:g, down:r, left:b, up:o, opp:w},
        r: {right:w, down:b, left:y, up:g, opp:o},
        o: {right:g, down:y, left:b, up:w, opp:r},
        b: {right:o, down:y, left:r, up:w, opp:g},
        g: {right:w, down:r, left:y, up:o, opp:b}
    }
    faceId2direction: dict[FaceId, dict[FaceId, Direction]] = { # mapping Face center color to SideDirection
        w: {o:right, b:down, r:left, g:up, y:opp},
        y: {g:right, r:down, b:left, o:up, w:opp},
        r: {w:right, b:down, y:left, g:up, o:opp},
        o: {g:right, y:down, b:left, w:up, r:opp},
        b: {o:right, y:down, r:left, w:up, g:opp},
        g: {w:right, r:down, y:left, o:up, b:opp}
    }

class Cube(CubeStructure):
    """Class(Structur and functions) of a 3x3 Rubick's Cube"""
    def __init__(self, size:int = 3, start_faceId: FaceId = w):
        """Initialize a Cube(Solved) of given size."""
        self.size: int = size
        self.state: dict[FaceId, Face] = Cube.getSolvedState(self.size)
        self.start_faceId: FaceId = start_faceId


    def __getitem__(self, face_id: FaceId) -> Face:
        return self.state[face_id]

    def __setitem__(self, face_id: FaceId, value: Face) -> None:
        self.state[face_id] = value

    def __contains__(self, face_id: FaceId) -> bool:
        return face_id in self.state

    movementDirection2index: dict[Direction, tuple[str, int]] = { # mapping movement of SideDirection to row/column index
        up: ('x', 0),
        down: ('x', -1),
        right: ('y', -1),
        left: ('y', 0)
    }
    sideDirection2edgeCoord: dict[Direction, Position] = { # Coordinate of edges in a face grid of 3x3 Cube
        up: Position(0,1),
        down: Position(2, 1),
        right: Position(1, 2),
        left: Position(1, 0)
    }
    cornerCoord: list[Position] = [
        Position(0, 0), Position(0, 2), Position(2, 2), Position(2, 0)
    ]

    @staticmethod
    def getSolvedState(size:int = 3, faceId2fillColor: Callable[[FaceId], Color] = lambda x: x)  -> dict[FaceId, Face]:
        """Return the solved state of a Cube of given size."""
        return {
            faceId: Face(size, faceId2fillColor(faceId))
            for faceId in Cube.faceIds
        }
    
    @staticmethod
    def BackEdgeCoords(position: Position) -> Position:
        """Given edge coordinates (i, j)(front), return the opposite(back) edge coordinates."""
        # implement edge check
        i, j = position
        if (i+j) == 3:
            return Position(i-1, j-1)
        else: #if edge then i+j == 1
            return Position(i+1, j+1)

    @staticmethod
    def EdgeOtherSide(coords: Coords) -> Coords:
        """Given coords of one side of an edge piece, 
        return the coords of the other side of that edge piece."""      
        face_id, i, j = coords
        ind = int(Cube.colors.index(face_id))
        k = (3 - (i + j))//2
        if (i + j)&1:
            # edges
            return Coords(Cube.colors[(ind + 1 + k*3 + ((ind + (i&1))&1))%6], k + (ind&1), k + ((ind + 1)&1))
        else:
            raise ValueError
        
    def isSolved(self) -> bool:
        """Check if the Cube is in solved state."""
        return self.state == Cube.getSolvedState(self.size)
    
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
    
    def clockwise(self, face_id: FaceId):
        self[face_id].rotate_clockwise()
        neighbors = self.get_neighbors(face_id)
        edges = [self[f].get_edge(d) for f, d in neighbors]
        
        for (f, d), new_edge in zip(neighbors, edges[1:] + edges[:1]): # change here for opposite rotation
            self[f].set_edge(d, new_edge)
        return Move(face_id)
    
    def anticlockwise(self, face_id: FaceId):
        self[face_id].rotate_clockwise()
        neighbors = self.get_neighbors(face_id)
        edges = [self[f].get_edge(d) for f, d in neighbors]
        
        for (f, d), new_edge in zip(neighbors, edges[-1:] + edges[:-1]): # change here for opposite rotation
            self[f].set_edge(d, new_edge)
        return Move(face_id)
    
    # def clockwise(self, face_id: FaceId):
    #     if isinstance(face_id, Move):
    #         # move = Move(move, 1)
    #         raise ValueError("Expected FaceId, got Move")
    #     new = deepcopy(self.state)
    #     color_index_inOrder_ruld = [
    #         # rig =
    #         (Cube.direction2faceId[face_id][right], Cube.movementDirection2index[Cube.faceId2direction[Cube.direction2faceId[face_id][right]][face_id]]),
    #         # u =
    #         (Cube.direction2faceId[face_id][up], Cube.movementDirection2index[Cube.faceId2direction[Cube.direction2faceId[face_id][up]][face_id]]),
    #         # lef =
    #         (Cube.direction2faceId[face_id][left], Cube.movementDirection2index[Cube.faceId2direction[Cube.direction2faceId[face_id][left]][face_id]]),
    #         # d =
    #         (Cube.direction2faceId[face_id][down], Cube.movementDirection2index[Cube.faceId2direction[Cube.direction2faceId[face_id][down]][face_id]])
    #     ]
    #     # print(color_index_inOrder_ruld)
    #     # rotating face,
    #     self[face_id].rotate_clockwise()
    #     # changing side faces
    #     for i in range(3):
    #         for j in range(3):
    #             new[color_index_inOrder_ruld[j][0]][color_index_inOrder_ruld[j][1][1] if color_index_inOrder_ruld[j][1][0] == 'x' else i][color_index_inOrder_ruld[j][1][1] if color_index_inOrder_ruld[j][1][0] == 'y' else i] = self.state[color_index_inOrder_ruld[j+1][0]][color_index_inOrder_ruld[j+1][1][1] if color_index_inOrder_ruld[j+1][1][0] == 'x' else i][color_index_inOrder_ruld[j+1][1][1] if color_index_inOrder_ruld[j+1][1][0] == 'y' else i]
    #             new[color_index_inOrder_ruld[3][0]][color_index_inOrder_ruld[3][1][1] if color_index_inOrder_ruld[3][1][0] == 'x' else i][color_index_inOrder_ruld[3][1][1] if color_index_inOrder_ruld[3][1][0] == 'y' else i] = self.state[color_index_inOrder_ruld[0][0]][color_index_inOrder_ruld[0][1][1] if color_index_inOrder_ruld[0][1][0] == 'x' else i][color_index_inOrder_ruld[0][1][1] if color_index_inOrder_ruld[0][1][0] == 'y' else i]
    #     self.state = new
    #     return Move(face_id)
 
    # def anticlockwise(self, face, numberOfTimes = 1):
    #     numberOfTimes = numberOfTimes%4
    #     if numberOfTimes == 0:
    #         return
    #     if numberOfTimes == 2:
    #         return self.clockwise(face,2)
    #     if numberOfTimes == 3:
    #         return self.clockwise(face)
    #     new = deepcopy(self.state)
    #     color_index_inOrder_dlur = [
    #         # rig =
    #         (Cube.direction2faceId[face][right], Cube.movementDirection2index[Cube.faceId2direction[Cube.direction2faceId[face][right]][face]]),
    #         # u =
    #         (Cube.direction2faceId[face][up], Cube.movementDirection2index[Cube.faceId2direction[Cube.direction2faceId[face][up]][face]]),
    #         # lef =
    #         (Cube.direction2faceId[face][left], Cube.movementDirection2index[Cube.faceId2direction[Cube.direction2faceId[face][left]][face]]),
    #         # d =
    #         (Cube.direction2faceId[face][down], Cube.movementDirection2index[Cube.faceId2direction[Cube.direction2faceId[face][down]][face]])
    #     ]
    #     color_index_inOrder_dlur.reverse()
    #     # rotating face,
    #     for i in range(3):
    #         for j in range(3):
    #             new[face][i][j] = self.state[face][j][2-i]
    #         # changing side faces
    #     for i in range(3):
    #         for j in range(3):
    #             new[color_index_inOrder_dlur[j][0]][color_index_inOrder_dlur[j][1][1] if color_index_inOrder_dlur[j][1][0] == 'x' else i][color_index_inOrder_dlur[j][1][1] if color_index_inOrder_dlur[j][1][0] == 'y' else i] = self.state[color_index_inOrder_dlur[j+1][0]][color_index_inOrder_dlur[j+1][1][1] if color_index_inOrder_dlur[j+1][1][0] == 'x' else i][color_index_inOrder_dlur[j+1][1][1] if color_index_inOrder_dlur[j+1][1][0] == 'y' else i]
    #             new[color_index_inOrder_dlur[3][0]][color_index_inOrder_dlur[3][1][1] if color_index_inOrder_dlur[3][1][0] == 'x' else i][color_index_inOrder_dlur[3][1][1] if color_index_inOrder_dlur[3][1][0] == 'y' else i] = self.state[color_index_inOrder_dlur[0][0]][color_index_inOrder_dlur[0][1][1] if color_index_inOrder_dlur[0][1][0] == 'x' else i][color_index_inOrder_dlur[0][1][1] if color_index_inOrder_dlur[0][1][0] == 'y' else i]
    #     self.state = new
    #     return face+'`'
    
    def scramble(self, sequence):
        return self.apply(g,w, sequence)
    
    def randomScramble(self, limit = 20):
        moves = []
        for _ in range(limit):
            moves.append(self.clockwise(random.choice(Cube.colors), random.choice([1,2,3])))
        return moves

    def __format__(self, format_spec: str) -> str:
        """
        Prints the cube layout starting from self.start_faceId in a diagonal layout:
            w
            b  o
               y  g
                  r
        Traverses down and right directions dynamically until right loops back to start.
        """
        def fmt(face_id):
            return format(self[face_id], format_spec).split('\n')

        face = self.start_faceId
        goDown = False
        gap = "  "  # space between adjacent faces in a row
        ans = []
        current_face = Cube.direction2faceId[face][down]

        # Helper to format a face as a list of lines
       # Determine width of a single face (for spacing)
        current_lines = fmt(face)
        face_width = len(current_lines[0])
        rightCount = 0
        
        while current_face != face:
            # collect faces in the current "row"
            if goDown:
                # ans += current_lines (already done in else case)
                current_face = Cube.direction2faceId[current_face][down]
                current_lines = fmt(current_face)
                
            else:
                ans += current_lines
                current_l = fmt(current_face)
                current_face = Cube.direction2faceId[current_face][right]
                if next_face == face:
                    next_lines = [""]*len(current_lines)
                else:
                    next_lines = fmt(next_face)
                indent = (" " * (face_width) + gap) * rightCount
                ans += [indent + current_lines[i] + gap + next_lines[i] for i in range(len(current_lines))]
                current_face = next_face
                goDown = True
            faces_in_row = []
            f = current_face
            while True:
                faces_in_row.append(f)
                next_right = self.direction2faceId[f].get(right)
                if not next_right or next_right == start:
                    break
                f = next_right

            # format each face
            formatted = [fmt(face) for face in faces_in_row]

            # horizontally combine faces in this row
            for row_i in range(len(formatted[0])):
                line = (' ' * indent) + gap.join(f[row_i] for f in formatted)
                face_lines.append(line)
            face_lines.append("")  # blank line between rows

            # move one step down
            next_down = self.direction2faceId[current_face].get(down)
            if not next_down or next_down == start:
                break
            indent += indent_step
            current_face = next_down

        return "\n".join(face_lines)

    __str__ = lambda self: self.__format__('i')

if __name__ == "__main__":
    cube = Cube()
    # print(cube.anticlockwise(w))
    # print(cube)

    print(cube.clockwise(r))
    # print(cube)

    # print(cube.anticlockwise(b,3))
    print(cube)

    print(cube.clockwise(o))
    print(cube)
