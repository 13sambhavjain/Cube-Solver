from copy import copy, deepcopy
import random
from shortnames import *
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
    cornerCoord = [
        (0, 0), (0, 2), (2, 2), (2, 0)
    ]
    
    def __init__(self, rows = 3, cols = 3, printState=False):
        self.rows = rows
        self.cols = cols
        self.state = {x: [[x for i in range(self.cols)] for j in range(self.rows)] for x in Cube.colors}
        if printState:
            print(self.state)

    @staticmethod
    def OppositeEdgeCoords(i, j):
        # implement edge check
        if (i+j) == 3:
            return i-1, j-1
        else: #if edge then i+j == 1
            return i+1, j+1
        
    def first_cross(self, first=w):
        # self = deepcopy(demoself)
        done = set()
        last = Cube.direction2color[first][opp]
        def color_on_top(i, j):
            if self.state[first][i][j] != first:
                raise ValueError
            otherSide = Cube.EotherSide(first, i, j)
            otherColor = self.state[otherSide[0]][otherSide[1]][otherSide[2]]
            if otherSide[0] == otherColor:
                done.add(otherColor)
                return list()
            if len(done) == 0:
                # rotate color logic
                fromSide = Cube.color2direction[first][otherSide[0]]
                toSide = Cube.color2direction[first][otherColor]
                done.add(otherColor)
                return [self.clockwise(first, Cube.directions.index(toSide) - Cube.directions.index(fromSide))]
            else:
                moves = [self.clockwise(otherSide[0], 2)] 
                li, lj = Cube.OppositeEdgeCoords(i, j)
                if self.state[last][li][lj] != first:
                    raise Exception
                return moves + color_on_bottom(li, lj)
        def color_on_bottom(i, j):
            otherSide = self.EotherSide(last, i, j)
            otherColor = self.state[otherSide[0]][otherSide[1]][otherSide[2]]
            fromSide = Cube.color2direction[last][otherSide[0]]
            toSide = Cube.color2direction[last][otherColor]
            done.add(otherColor)
            return [self.clockwise(last, Cube.directions.index(toSide) - Cube.directions.index(fromSide)), self.clockwise(otherColor, 2)]
        
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
                return [self.clockwise(first, r1), self.clockwise(otherSide[0], r2), self.anticlockwise(first, r1)]
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
                    moves.append(self.anticlockwise(c, rotate)) #changed from clock - to - anticlock
                done.add(otherColor)
                return moves

            if otherSide[0] == first:
                return color_on_side_top()
            elif otherSide[0] == last:
                return color_on_side_bottom()
            else:
                return color_on_side_mid()
        # while len(done) < 4:
        cross_moves = list()
        while(len(done) < 4):
            for c in self.state:
                for i in range(3):
                    for j in range(3):
                        if (i+j)&1 and self.state[c][i][j] == first:
                            if c == first:
                                cross_moves += color_on_top(i, j)
                            elif c == last:
                                cross_moves += color_on_bottom(i,j)
                            else:
                                cross_moves += color_on_side(c, i, j)

        return cross_moves
    
    def first_corners(self, first=w):
        # self = deepcopy(demoself)
        done = set()
        last = Cube.direction2color[first][opp]
        def color_on_top(i, j):
            if self.state[first][i][j] != first:
                raise ValueError
            otherSide1, otherSide2 = Cube.CotherSide(first, i, j)
            otherColor1 = self.state[otherSide1[0]][otherSide1[1]][otherSide1[2]]
            otherColor2 = self.state[otherSide2[0]][otherSide2[1]][otherSide2[2]]
            if otherSide1[0] == otherColor1:
                done.add((otherColor1, otherColor2))
                return list()
            else:
                d1 = Cube.color2direction[first][otherColor1]
                d2 = Cube.color2direction[first][otherColor2]
                i1 = Cube.directions.index(d1)
                i2 = Cube.directions.index(d2)
                faceToRotate = otherSide1[0]
                if (i2 - i1)%4 == 1:
                    faceToRotate = otherSide2[0]
                elif (i1-i2)%4 != 3:
                    raise Exception (f'{otherColor1}, {otherColor2} and {first} dont share a corner.')
                
                
                shiftsTo = Cube.cornerAfterRotation(Cube.cornerAfterRotation((first, i, j), faceToRotate), last)
                return [self.clockwise(faceToRotate), self.clockwise(last), self.anticlockwise(faceToRotate)] + color_on_side(*shiftsTo)
                # Just removes corner from the first face, and puts it on the desired row (side bottom)
        def color_on_bottom(i, j):
            otherSide = self.EotherSide(last, i, j)
            otherColor = self.state[otherSide[0]][otherSide[1]][otherSide[2]]
            fromSide = Cube.color2direction[last][otherSide[0]]
            toSide = Cube.color2direction[last][otherColor]
            done.add(otherColor)
            return [self.clockwise(last, Cube.directions.index(toSide) - Cube.directions.index(fromSide)), self.clockwise(otherColor, 2)]
            pass
        def color_on_side(c, i, j):
            otherSide = Cube.EotherSide(c, i, j)
            otherColor = self.state[otherSide[0]][otherSide[1]][otherSide[2]]
            def color_on_side_top():
                otherSide1, otherSide2 = Cube.CotherSide(first, i, j)
                otherColor1 = self.state[otherSide1[0]][otherSide1[1]][otherSide1[2]]
                otherColor2 = self.state[otherSide2[0]][otherSide2[1]][otherSide2[2]]
                if otherSide1[0] == otherColor1:
                    done.add((otherColor1, otherColor2))
                    return list()
                else:
                    d1 = Cube.color2direction[first][otherColor1]
                    d2 = Cube.color2direction[first][otherColor2]
                    i1 = Cube.directions.index(d1)
                    i2 = Cube.directions.index(d2)
                    faceToRotate = otherSide1[0]
                    if (i2 - i1)%4 == 1:
                        faceToRotate = otherSide2[0]
                    elif (i1-i2)%4 != 3:
                        raise Exception (f'{otherColor1}, {otherColor2} and {first} dont share a corner.')
                    
                    return [self.clockwise(faceToRotate), self.clockwise(last), self.anticlockwise(faceToRotate)]
            def color_on_side_mid():
                fromSide = Cube.color2direction[first][otherColor]
                toSide = Cube.color2direction[first][otherSide[0]]
                r1 = (Cube.directions.index(toSide) - Cube.directions.index(fromSide))
                otherFrom = Cube.color2direction[otherSide[0]][c]
                otherTo = Cube.color2direction[otherSide[0]][first]
                r2 = (Cube.directions.index(otherTo) - Cube.directions.index(otherFrom))
                done.add(otherColor)
                return ["sdfasfad", self.clockwise(first, r1), self.clockwise(otherSide[0], r2), self.anticlockwise(first, r1)]
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
                    moves.append(self.anticlockwise(c, rotate)) #changed from clock - to - anticlock
                done.add(otherColor)
                return moves

            if otherSide[0] == first:
                return color_on_side_top()
            elif otherSide[0] == last:
                return color_on_side_bottom()
            else:
                return color_on_side_mid()
        # while len(done) < 4:
        cross_moves = list()
        while(len(done) < 4):
            for c in self.state:
                for i in range(3):
                    for j in range(3):
                        if (i+j)&1 and self.state[c][i][j] == first:
                            if c == first:
                                cross_moves += [(c,i,j),"cot",color_on_top(i, j)]
                            elif c == last:
                                cross_moves += [(c,i,j),"cob",color_on_bottom(i,j)]
                            else:
                                cross_moves += [(c,i,j),"cos",color_on_side(c, i, j)]
        return cross_moves
    
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
        rotate = Cube.directions.index(Cube.color2direction[front][top])
        di = {
            'U': Cube.direction2color[front][Cube.directions[rotate]],
            'R': Cube.direction2color[front][Cube.directions[(rotate+1)%4]],
            'D': Cube.direction2color[front][Cube.directions[(rotate+2)%4]],
            'L': Cube.direction2color[front][Cube.directions[(rotate+3)%4]],
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
   
    def applyScramble(self, sequence):
        return self.apply(g, w, sequence)

    def random(self, limit=10):
        moves = []
        for _ in range(limit):
            moves.append(self.clockwise(random.choice(Cube.colors), random.randint(1,3)))
        return moves

    def turnFaces(self, faces: list[str]):
        for face in faces:
            if face[-1] in ["'", '`']:
                self.anticlockwise(face[:-1])
            else:
                self.clockwise(face)
    
    def turnFaceNumericNotation(self, moves):
        for face in moves:
            self.clockwise(*face)

    @classmethod
    def formulas2Faces(cls, front, top, *formulas) -> list[str]:
        moves = []
        rotate = Cube.directions.index(Cube.color2direction[front][top])
        di = {
            'U': Cube.direction2color[front][Cube.directions[rotate]],
            'R': Cube.direction2color[front][Cube.directions[(rotate+1)%4]],
            'D': Cube.direction2color[front][Cube.directions[(rotate+2)%4]],
            'L': Cube.direction2color[front][Cube.directions[(rotate+3)%4]],
            'B': Cube.direction2color[front][opp],
            'F': front
        }
        for formula in formulas:
            i = 0
            n = len(formula) - 1
            while i < n:
                if formula[i+1] in ['`', "'"]:
                    moves.append(di[formula[i]])
                    i += 2
                else:
                    moves.append(di[formula[i]])
                    i += 1
            if i == n:
                moves.append(di[formula[i]])
        return moves

    def __str__(self):
        return str(self.state)

    @staticmethod
    def cornerAfterRotation(coords, rotatingFace, check=True):
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
    def get_solved_cube(row, col):
        return {x: [[x for i in range(col)] for j in range(row)] for x in Cube.colors}
   
    @staticmethod
    def EotherSide(color, i, j):
            # edge
            # if i == 0 and j == 1:
            #     Cube.colors[(ind + 1 + 3)%6], 1, 2     # ind + 4 + ind&1, 1 + ind&1, 1 + (ind + 1)&1
            #     Cube.colors[(ind + 2 + 3)%6], 2, 1
            # if i == 1 and j == 0:
            #     Cube.colors[(ind + 2 + 3)%6], 1, 2     # ind + 4 + (ind + 1)&1,
            #     Cube.colors[(ind + 1 + 3)%6], 2, 1
            # if i == 1 and j == 2:
            #     Cube.colors[(ind + 2)%6], 0, 1         # ind + 1 + (ind + 1)&1
            #     Cube.colors[(ind + 1)%6], 1, 0
            # if i == 2 and j == 1:
            #     Cube.colors[(ind + 1)%6], 0, 1         # ind + 1 + ind&1
            #     Cube.colors[(ind + 2)%6], 1, 0        
        ind = int(Cube.colors.index(color))
        k = (3 - (i + j))//2
        if (i + j)&1:
            # edges
            return Cube.colors[(ind + 1 + k*3 + ((ind + (i&1))&1))%6], k + (ind&1), k + ((ind + 1)&1)
        else:
            raise ValueError

    @staticmethod
    def CotherSide(c, i, j):
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
   
    def checkFirstCross(self, first=w) -> bool:
        for i, j in Cube.edgeCoord.values():
            if self.state[first][i][j] != first:
                return False
        return True
   
    def __getitem__(self, key):
        return self.state[key]
    
def testFun(applyFun, checkFun, numberOfCases=1000, scrambleLimit = 10):
    fails = []
    for case in range(numberOfCases):
        c = Cube()
        scram = c.random(scrambleLimit)
        funMoves = applyFun(c)
        if not checkFun(c):
            return dict(scram=scram, moves=funMoves)
            break
    return fails

def test2(applyFun, checkFun, numberOfCases=1000, scrambleLimit = 10):
    fails = []
    for case in range(numberOfCases):
        print(case)
        c = Cube()
        scram = c.random(scrambleLimit)
        funMoves = applyFun(c)
        if not checkFun(c):
            return dict(scram1=scram, moves1=funMoves)
        scram2 = makeScrambleEfficient(scram)
        funMoves2 = makeScrambleEfficient(funMoves)
        c1 = Cube()
        c1.turnFaceNumericNotation(scram2)
        c1.turnFaceNumericNotation(funMoves2)
        if not checkFun(c1):
            return dict(scram2=scram, moves2=funMoves) + dict(scram1=scram, moves1=funMoves)
    return fails

def D_Nest_scamble(scramble):
    moves = []
    for move in scramble:
        if isinstance(move, (tuple, list)):
            for k in move:
                moves.append(k)
        elif isinstance(move, str):
            moves.append(move)
    return moves

def NumericMovesNotation(scramble):
    moves = []
    for move in scramble:
        if move[-1] in ["`", "'"]:
            moves.append((move[:-1], -1))
        else:
            moves.append((move, 1))
    return moves

def makeScrambleEfficient(scramble):
    if len(scramble) < 1:
        return []
    scramble = NumericMovesNotation(D_Nest_scamble(scramble))
    moves = [scramble[0]]
    for move in scramble[1:]:
        if len(moves) > 0 and move[0] == moves[-1][0]:
            k = (move[1]+moves[-1][1])%4
            if k == 0:
                del moves[-1]
                continue
            elif k == 3:
                k = -1
            moves[-1] = (move[0], k)
        else:
            moves.append(move)
    return moves

def CorrectSolForScramble(scramble):
    c = Cube()
    moves = D_Nest_scamble(scramble)
    c.turnFaces(moves)
    sol = makeScrambleEfficient(c.first_cross())
    print(scramble)
    print(sol)
    print(c.checkFirstCross())
    print(c[w])


    
    
    


# tt = test2(Cube.first_cross, Cube.checkFirstCross, 100000, 20)
# print(tt)

# def move(self, move):

# c.clockwise(g)
# c.anticlockwise(w)
# c.clockwise(w)
# print(c.otherSide(w, 1, 2))
# edge = set()
# opp = set()
# for color, mat in c.state.items():
# for i, j in [(0,1), (1,0), (1, 2), (2,1)]:
# x = (color, i, j)
# edge.add(x)
# y = c.otherSide(*x)
# opp.add(y)
# print(*x, ': ', y)
# if x != c.otherSide(*y):
# print("Something is wrong here")
# c = Cube()

# c.first_cross()
# c.apply(o, y, 'RUR`URUUR`'*6)

# print(c)
# if edge == opp:
# print("Ya seems equal")

# from TestFailScrambles import FirstCrossFails
# scramble = FirstCrossFails[1]
# CorrectSolForScramble(scramble)


# for c in Cube.colors:
#     for i, j in Cube.cornerCoord:
#         # print(Cube.CotherSide(c,i,j))
#         for r1 in Cube.colors:
#             k = Cube.cornerAfterRotation((c, i, j), r1)
#             if k != (c, i, j):
#                 print((c, i, j), r1, k)

