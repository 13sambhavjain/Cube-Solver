from CubeClass import Cube
from Directions import Direction, SideDirections
from Colors import Color, Colors
from ColorDirectionAcronyms import *
from copy import deepcopy


class Solver(Cube):

    
        
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
    
    def apply(self, front, top, *formulas) -> list:
        moves = []
        rotate = Cube.side_directions.index(Cube.color2direction[front][top])
        di = {
            'U': Cube.direction2color[front][Cube.side_directions[rotate]],
            'R': Cube.direction2color[front][Cube.side_directions[(rotate+1)%4]],
            'D': Cube.direction2color[front][Cube.side_directions[(rotate+2)%4]],
            'L': Cube.direction2color[front][Cube.side_directions[(rotate+3)%4]],
            'B': Cube.direction2color[front][opp],
            'F': front
        }
        for formula in formulas:
            i = 0
            n = len(formula) - 1
            while i < n:
                if formula[i+1] in ['`', "'"]:
                    moves.append(self.anticlockwise(di[formula[i]]))
                    i += 2
                else:
                    moves.append(self.clockwise(di[formula[i]]))
                    i += 1
            if i == n:
                moves.append(self.clockwise(di[formula[i]]))
        return moves


