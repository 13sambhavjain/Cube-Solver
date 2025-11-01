from copy import copy, deepcopy
import random
from Colors import *
# colors = [w,r,g,y,o,b]
# sturcture =   # w
                # b o
                  # y g
                    # r
 
class Cube():
    colors = [w,b,o,y,g,r]
    directions = [up, right, down, left]
    direction2color = {
        w: {right:o, down:b, left:r, up:g, opp:y},
        y: {right:g, down:r, left:b, up:o, opp:w},
        r: {right:w, down:b, left:y, up:g, opp:o},
        o: {right:g, down:y, left:b, up:w, opp:r},
        b: {right:o, down:y, left:r, up:w, opp:g},
        g: {right:w, down:r, left:y, up:o, opp:b}
    }
    color2direction = {
        w: {o:right, b:down, r:left, g:up, y:opp},
        y: {g:right, r:down, b:left, o:up, w:opp},
        r: {w:right, b:down, y:left, g:up, o:opp},
        o: {g:right, y:down, b:left, w:up, r:opp},
        b: {o:right, y:down, r:left, w:up, g:opp},
        g: {w:right, r:down, y:left, o:up, b:opp}
    }
    movementDirection2index = {
        up: ('r', 0),
        down: ('r', -1),
        right: ('c', -1),
        left: ('c', 0)
    }
    edgeCoord = {
        up: (0,1),
        down: (2, 1),
        right: (1, 2),
        left: (1, 0)
    }
    def solved(self, rows = 3, cols = 3) -> bool:
        if self.state == {x: [[x for i in range(self.cols)] for j in range(self.rows)] for x in Cube.colors}:
            return True
        else:
            return False
    def __init__(self, rows = 3, cols = 3):
        self.rows = rows
        self.cols = cols
        self.state = {x: [[x for i in range(self.cols)] for j in range(self.rows)] for x in Cube.colors}
        # print(self.state)
 
    def first_cross(demoself, first=w):
        self = deepcopy(demoself)
        done = set()
        last = Cube.direction2color[first][opp]
        def color_on_top(i, j):
            if self.state[first][i][j] != first:
                raise ValueError
            otherSide = Cube.EotherSide(first, i, j)
            otherColor = self.state[otherSide[0]][otherSide[1]][otherSide[2]]
            if otherSide[0] == otherColor:
                done.add(otherColor)
                return
            if len(done) == 0:
                # rotate color logic
                fromSide = Cube.color2direction[first][otherSide[0]]
                toSide = Cube.color2direction[first][otherColor]
                done.add(otherColor)
                return self.clockwise(first, Cube.directions.index(toSide) - Cube.directions.index(fromSide))
            else:
                return self.clockwise(otherSide[0], 2) + color_on_bottom(*Cube.edgeCoord[Cube.color2direction[last][otherSide[0]]]) 
        def color_on_bottom(i, j):
            otherSide = self.EotherSide(last, i, j)
            otherColor = self.state[otherSide[0]][otherSide[1]][otherSide[2]]
            fromSide = Cube.color2direction[last][otherSide[0]]
            toSide = Cube.color2direction[last][otherColor]
            done.add(otherColor)
            return self.clockwise(last, Cube.directions.index(toSide) - Cube.directions.index(fromSide)), self.clockwise(otherColor, 2)
            pass
        def color_on_side(c, i, j):
            otherSide = Cube.EotherSide(c, i, j)
            otherColor = self.state[otherSide[0]][otherSide[1]][otherSide[2]]
            def color_on_side_top():
                fromSide = Cube.color2direction[first][c]
                toSide = Cube.color2direction[first][otherColor]
                rotate = (Cube.directions.index(toSide) - Cube.directions.index(fromSide))
                rotate %= 4 # rotating first for fromSide to reach toSide
                done.add(otherColor)
                if rotate == 3:
                    return self.apply(c,first, 'FR')
                if rotate == 2:
                    return self.apply(c,first, 'FURU`')
                if rotate == 1:
                    return self.apply(c,first, 'F`L`')
                if rotate == 0:
                    return self.apply(c,first, 'FU`RU')
            def color_on_side_mid():
                fromSide = Cube.color2direction[first][otherColor]
                toSide = Cube.color2direction[first][otherSide[0]]
                r1 = (Cube.directions.index(toSide) - Cube.directions.index(fromSide))
                otherFrom = Cube.color2direction[otherSide[0]][c]
                otherTo = Cube.color2direction[otherSide[0]][first]
                r2 = (Cube.directions.index(otherTo) - Cube.directions.index(otherFrom))
                done.add(otherColor)
                return self.clockwise(first, r1), self.clockwise(otherSide[0], r2), self.anticlockwise(first, r1)
            def color_on_side_bottom():
                # fromSide = Cube.color2direction[first][otherColor]
                moves = None
                if otherColor == c:
                    return self.apply(c, first, 'F`U`RU')
                if otherColor == Cube.direction2color[c][opp]:
                    moves = self.apply(c, first, 'F`URU`')
                    if c in done:
                        moves.append(self.clockwise(c))
                    return moves
                fromSide = Cube.color2direction[c][last]
                toSide = Cube.color2direction[c][otherColor]
                rotate = (Cube.directions.index(toSide) - Cube.directions.index(fromSide))%4
                fromSide1 = Cube.color2direction[otherColor][c]
                toSide1 = Cube.color2direction[otherColor][first]
                rotate1 = (Cube.directions.index(toSide1) - Cube.directions.index(fromSide1))%4
                moves = [
                    self.clockwise(c, rotate),
                    self.clockwise(otherColor, rotate1)
                ]
                if c in done:
                    moves.append(self.clockwise(c, rotate))
                return moves
 
            if otherSide[0] == first:
                return color_on_side_top()
            elif otherSide[0] == last:
                return color_on_side_bottom()
            else:
                return color_on_side_mid()
        # while len(done) < 4:
        for c in self.state:
            for i in range(3):
                for j in range(3):
                    if (i+j)&1 and self.state[c][i][j] == first:
                        # print(c, i, j)
                        if c == first:
                            color_on_top(i, j)
                        elif c == last:
                            color_on_bottom(i,j)
                        else:
                            color_on_side(c, i, j)
        # print(done)
 
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



