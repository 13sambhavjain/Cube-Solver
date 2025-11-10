from copy import copy, deepcopy
import random
from Colors import Colors, Color
from Face import Face, FaceId, FaceIds, Position, Coords
from Directions import SideDirections, Direction
from Moves import Move, Moves
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
    side_directions = SideDirections() # [up, right, down, left] - with some cyclic Functionalities
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
    movementDirection2index: dict[Direction, tuple[str, int]] = { # mapping movement of SideDirection to row/column index
        up: ('x', 0),
        down: ('x', -1),
        right: ('y', -1),
        left: ('y', 0)
    }
    @staticmethod
    def formula2Moves(front: FaceId, top: FaceId, formula: str) -> Moves:
        moves = Moves()
        rotate = CubeStructure.side_directions.index(CubeStructure.faceId2direction[front][top])
        direction_map: dict[str, FaceId] = {
            'U': CubeStructure.direction2faceId[front][CubeStructure.side_directions[rotate]],
            'R': CubeStructure.direction2faceId[front][CubeStructure.side_directions[(rotate+1)%4]],
            'D': CubeStructure.direction2faceId[front][CubeStructure.side_directions[(rotate+2)%4]],
            'L': CubeStructure.direction2faceId[front][CubeStructure.side_directions[(rotate+3)%4]],
            'B': CubeStructure.direction2faceId[front][opp],
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

class Cube(CubeStructure):
    """Class(Structur and functions) of a 3x3 Rubick's Cube"""

    sideDirection2edgePosition: dict[Direction, Position] = { # Coordinate of edges in a face grid of 3x3 Cube
        up: Position(0,1),
        down: Position(2, 1),
        right: Position(1, 2),
        left: Position(1, 0)
    }
    cornerCoord: list[Position] = [
        Position(0, 0), Position(0, 2), Position(2, 2), Position(2, 0)
    ]

    def __init__(self, size:int = 3, start_faceId: FaceId = w, *, default_print_format: str = 'i'):
        """Initialize a Cube(Solved) of given size."""
        self.size: int = size
        self.state: dict[FaceId, Face] = Cube.getSolvedState(self.size)
        self.start_faceId: FaceId = start_faceId
        self.default_print_format: str = default_print_format

    def apply_formula(self, front: FaceId = w, top: FaceId = w, *formulas: str) -> Moves:
        moves = Moves()
        for formula in formulas:
            current_moves = CubeStructure.formula2Moves(front, top, formula)
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
        moves = Cube.get_randomScramble(limit)
        return self.apply_moves(moves)
    
    @staticmethod
    def get_randomScramble(limit: int = 20) -> Moves:
        moves: Moves = Moves()
        for _ in range(limit):
            moves.append(Move(faceId=random.choice(Cube.faceIds), turns=random.choice([1,2,3])))
        return moves
    
    def isSolved(self) -> bool:
        """Check if the Cube is in solved state."""
        return self.state == Cube.getSolvedState(self.size)
    
    def __getitem__(self, face_id: FaceId) -> Face:
        return self.state[face_id]

    def __setitem__(self, face_id: FaceId, value: Face) -> None:
        self.state[face_id] = value

    def __contains__(self, face_id: FaceId) -> bool:
        return face_id in self.state

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
        def visible_len(s: str) -> int:
            """Return visible length of string ignoring ANSI color codes."""
            n = 0
            i = 0
            while i < len(s):
                if s[i] == "\x1b":  # start of ANSI escape sequence
                    # skip until 'm' or end of string
                    i += 1
                    while i < len(s) and s[i] != "m":
                        i += 1
                    i += 1  # skip the 'm' itself
                else:
                    n += 1
                    i += 1
            return n

        cameDown = False if Cube.faceIds.index(self.start_faceId)%2 else True
        gap = "  "  # space between adjacent faces in a row
        rightCount = 0
        start_face = self.start_faceId
        current_face = Cube.direction2faceId[start_face][down if cameDown else right]
        current_lines = fmt(start_face)
        face_width = visible_len(current_lines[0])
        ans = []
            
        while current_face != start_face:
            # collect faces in the current "row"
            if cameDown:
                ans += current_lines + [""]
                current_lines = fmt(current_face)
                indent = (" " * (face_width) + gap) * rightCount
                for i in range(len(current_lines)):
                    current_lines[i] = indent + current_lines[i]
                current_face = Cube.direction2faceId[current_face][right] #went to right
                cameDown = False
            else: # came right
                # ans += current_lines (already done in else case)
                add2lines = fmt(current_face)
                for i in range(len(current_lines)):
                    current_lines[i] += gap + add2lines[i]
                current_face = Cube.direction2faceId[current_face][down] # went down
                cameDown = True
                rightCount += 1
                
        ans += current_lines

        return "\n".join(ans)
    
    def __str__(self) -> str:
        return self.__format__(self.default_print_format)
    
    @staticmethod
    def getSolvedState(size:int = 3, faceId2fillColor: Callable[[FaceId], Color] = lambda x: x)  -> dict[FaceId, Face]:
        """Return the solved state of a Cube of given size."""
        return {
            faceId: Face(size, faceId2fillColor(faceId))
            for faceId in Cube.faceIds
        }
    
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
        ind = int(Cube.colors.index(face_id))
        k = (3 - (i + j))//2
        if (i + j)&1:
            # edges
            return Coords(Cube.colors[(ind + 1 + k*3 + ((ind + (i&1))&1))%6], k + (ind&1), k + ((ind + 1)&1))
        else:
            raise ValueError
    
    @staticmethod
    def CotherSide(c, i, j):
        raise NotImplementedError
        # corner
        cornerColors = [
            {(w, 0, 0), (g, 2, 2), (r, 0, 2)},
            {(w, 0, 2), (o, 0, 2), (g, 0, 2)},
            {(w, 2, 0), (b, 0, 0), (r, 2, 2)},
            {(w, 2, 2), (b, 0, 2), (o, 0, 0)},
            {(y, 0, 0), (b, 2, 2), (o, 2, 0)},
            {(y, 0, 2), (o, 2, 2), (g, 0, 0)},
            {(y, 2, 0), (b, 2, 0), (r, 2, 0)},
            {(y, 2, 2), (g, 2, 0), (r, 0, 0)}
        ]
        for colors in cornerColors:
            if (c, i, j) in colors:
                return colors - {(c, i, j)}
        else:
            raise ValueError(f'Given coords are not of a corner {(c,i,j)}')
        # ind = int(Cube.colors.index(color))
            # if i == 0 and j == 0:
            #     [(Cube.colors[(ind - 2)], 2, 2),
            #     (Cube.colors[(ind - 1)], 2*(ind&1), 2*((ind+1)&1))]

            # if i == 2 and j == 2:
            #     [(Cube.colors[(ind - 4)], 0, 0),
            #     (Cube.colors[(ind - 5)], 2*(ind&1), 2*((ind+1)&1))]

            # if i == 0 and j == 2:
            #     if ind&1:
                    
            # if i == 2 and j == 1:
            #     Cube.colors[(ind + 1)%6], 0, 1         # ind + 1 + ind&1
            #     Cube.colors[(ind + 2)%6], 1, 0        
        # k = (3 - (i + j))//2
        # if (i + j)&1:
        #     # edges
        #     return Cube.colors[(ind + 1 + k*3 + ((ind + (i&1))&1))%6], k + (ind&1), k + ((ind + 1)&1)
        # else:
        #     raise ValueError

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
    
if __name__ == "__main__":
    cube = Cube(start_faceId=b,default_print_format='coloredinitial')
    moves = cube.apply_formula(w, g, 'RUR`URUUR`')
    print(cube, moves)
    moves = cube.apply_formula(y, g, 'RUR`URUUR`UU')
    print(cube, moves)
    moves = cube.apply_formula(y, g, 'RUR`URUUR`')
    print(cube, moves)
    # moves = cube.apply_formula(o, g, 'RUR`URUUR`')
    # moves = cube.apply_formula(w, g, 'RUR`URUUR`')
    # moves = cube.apply_formula(y, g, 'RUR`URUUR`')
    # for move in moves:
    #     cube.make_move(move)
    #     print(move, cube, sep='\n')
    # print("*********************************************")
    # moves = cube.formula2Moves(y, g, 'RUR`URUUR`')
    # for move in moves:
    #     cube.make_move(move)
    #     print(move, cube, sep='\n')
