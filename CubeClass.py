from copy import copy, deepcopy
import random
from Colors import Colors, Color
from Face import Face
from Directions import SideDirections, Direction
from old_Colors import *
# colors = [w,r,g,y,o,b]
# sturcture =   # w
                # b o
                  # y g
                    # r
 
class Cube():

    colors = Colors() # [w, b, r, g, y, o] -  with some cyclic Functionalities
    directions = SideDirections() # [up, right, down, left] - with some cyclic Functionalities

    direction2color: dict[Color, dict[Direction, Color]] = { # mapping SideDirection to Face center color
        w: {right:o, down:b, left:r, up:g, opp:y},
        y: {right:g, down:r, left:b, up:o, opp:w},
        r: {right:w, down:b, left:y, up:g, opp:o},
        o: {right:g, down:y, left:b, up:w, opp:r},
        b: {right:o, down:y, left:r, up:w, opp:g},
        g: {right:w, down:r, left:y, up:o, opp:b}
    }
    color2direction: dict[Color, dict[Color, Direction]] = { # mapping Face center color to SideDirection
        w: {o:right, b:down, r:left, g:up, y:opp},
        y: {g:right, r:down, b:left, o:up, w:opp},
        r: {w:right, b:down, y:left, g:up, o:opp},
        o: {g:right, y:down, b:left, w:up, r:opp},
        b: {o:right, y:down, r:left, w:up, g:opp},
        g: {w:right, r:down, y:left, o:up, b:opp}
    }
    movementDirection2index: dict[Direction, tuple[str, int]] = { # mapping movement of SideDirection to row/column index
        up: ('r', 0),
        down: ('r', -1),
        right: ('c', -1),
        left: ('c', 0)
    }

    cornerCoord: list[tuple[int, int]] = [ # Coordinates of corners in a face grid of a Cube
        (0, 0), (0, 2), (2, 2), (2, 0)
    ] 
    
    def __init__(self, size:int = 3, printState: bool=False):
        """Initialize a Cube(Solved) of given size."""
        self.size: int = size
        self.state: dict[Color, Face] = Cube.getSolvedState(self.size)
        if printState:
            print(self.state)

    @staticmethod
    def getSolvedState(size:int = 3) -> dict[Color, Face]:
        """Return the solved state of a Cube of given size."""
        return {
            color: Face(color, size)
            for color in Cube.colors
        }
    
    def isSolved(self) -> bool:
        """Check if the Cube is in solved state."""
        return self.state == Cube.getSolvedState(self.size)
        
    def clockwise(self, face, numberOfTimes = 1):
        numberOfTimes = numberOfTimes%4
        if numberOfTimes == 0:
            return
        if numberOfTimes == 2:
            return self.clockwise(face), self.clockwise(face)
        if numberOfTimes == 3:
            return self.anticlockwise(face)
        new = deepcopy(self.state)
        # if face == w:
        #     for i in range(3):
        #         print(id(new[o][0][i]), id(new[o][1][i]))
        #         new[o][0][i] = self.state[g][i][2]
        #         new[g][i][2] = self.state[r][i][2]
        #         new[r][i][2] = self.state[b][0][i]
        #         new[b][0][i] = self.state[o][0][i]
        color_index_inOrder_ruld = [
            # rig =
            (Cube.direction2color[face][right], Cube.movementDirection2index[Cube.color2direction[Cube.direction2color[face][right]][face]]),
            # u =
            (Cube.direction2color[face][up], Cube.movementDirection2index[Cube.color2direction[Cube.direction2color[face][up]][face]]),
            # lef =
            (Cube.direction2color[face][left], Cube.movementDirection2index[Cube.color2direction[Cube.direction2color[face][left]][face]]),
            # d =
            (Cube.direction2color[face][down], Cube.movementDirection2index[Cube.color2direction[Cube.direction2color[face][down]][face]])
        ]
        # print(color_index_inOrder_ruld)
        # rotating face,
        for i in range(3):
            for j in range(3):
                new[face][i][j] = self.state[face][2-j][i]
        # changing side faces
        for i in range(3):
            for j in range(3):
                new[color_index_inOrder_ruld[j][0]][color_index_inOrder_ruld[j][1][1] if color_index_inOrder_ruld[j][1][0] == 'r' else i][color_index_inOrder_ruld[j][1][1] if color_index_inOrder_ruld[j][1][0] == 'c' else i] = self.state[color_index_inOrder_ruld[j+1][0]][color_index_inOrder_ruld[j+1][1][1] if color_index_inOrder_ruld[j+1][1][0] == 'r' else i][color_index_inOrder_ruld[j+1][1][1] if color_index_inOrder_ruld[j+1][1][0] == 'c' else i]
                new[color_index_inOrder_ruld[3][0]][color_index_inOrder_ruld[3][1][1] if color_index_inOrder_ruld[3][1][0] == 'r' else i][color_index_inOrder_ruld[3][1][1] if color_index_inOrder_ruld[3][1][0] == 'c' else i] = self.state[color_index_inOrder_ruld[0][0]][color_index_inOrder_ruld[0][1][1] if color_index_inOrder_ruld[0][1][0] == 'r' else i][color_index_inOrder_ruld[0][1][1] if color_index_inOrder_ruld[0][1][0] == 'c' else i]
        self.state = new
        return face
 
    def anticlockwise(self, face, numberOfTimes = 1):
        numberOfTimes = numberOfTimes%4
        if numberOfTimes == 0:
            return
        if numberOfTimes == 2:
            return self.clockwise(face,2)
        if numberOfTimes == 3:
            return self.clockwise(face)
        new = deepcopy(self.state)
        color_index_inOrder_dlur = [
            # rig =
            (Cube.direction2color[face][right], Cube.movementDirection2index[Cube.color2direction[Cube.direction2color[face][right]][face]]),
            # u =
            (Cube.direction2color[face][up], Cube.movementDirection2index[Cube.color2direction[Cube.direction2color[face][up]][face]]),
            # lef =
            (Cube.direction2color[face][left], Cube.movementDirection2index[Cube.color2direction[Cube.direction2color[face][left]][face]]),
            # d =
            (Cube.direction2color[face][down], Cube.movementDirection2index[Cube.color2direction[Cube.direction2color[face][down]][face]])
        ]
        color_index_inOrder_dlur.reverse()
        # rotating face,
        for i in range(3):
            for j in range(3):
                new[face][i][j] = self.state[face][j][2-i]
            # changing side faces
        for i in range(3):
            for j in range(3):
                new[color_index_inOrder_dlur[j][0]][color_index_inOrder_dlur[j][1][1] if color_index_inOrder_dlur[j][1][0] == 'r' else i][color_index_inOrder_dlur[j][1][1] if color_index_inOrder_dlur[j][1][0] == 'c' else i] = self.state[color_index_inOrder_dlur[j+1][0]][color_index_inOrder_dlur[j+1][1][1] if color_index_inOrder_dlur[j+1][1][0] == 'r' else i][color_index_inOrder_dlur[j+1][1][1] if color_index_inOrder_dlur[j+1][1][0] == 'c' else i]
                new[color_index_inOrder_dlur[3][0]][color_index_inOrder_dlur[3][1][1] if color_index_inOrder_dlur[3][1][0] == 'r' else i][color_index_inOrder_dlur[3][1][1] if color_index_inOrder_dlur[3][1][0] == 'c' else i] = self.state[color_index_inOrder_dlur[0][0]][color_index_inOrder_dlur[0][1][1] if color_index_inOrder_dlur[0][1][0] == 'r' else i][color_index_inOrder_dlur[0][1][1] if color_index_inOrder_dlur[0][1][0] == 'c' else i]
        self.state = new
        return face+'`'
    
    def scramble(self, sequence):
        return self.apply(g,w, sequence)
    
    def randomScramble(self, limit = 20):
        moves = []
        for _ in range(limit):
            moves.append(self.clockwise(random.choice(Cube.colors), random.choice([1,2,3])))
        return moves



