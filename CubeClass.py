from copy import copy, deepcopy
from Colors import *

# colors = [w,r,g,y,o,b]
# sturcture =   # w
                # b   o
                #     y   g
                #         r
class Cube():
    colors = [w,b,o,y,g,r]
    directions = [up, right, down, left]
    direction2color = {
        w: {right:o, down:b, left:r, up:g, opp:y},
        y: {right:g, down:r, left:b, up:o, opp:w},
        r: {right:r, down:b, left:y, up:g, opp:o},
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
    def __init__(self, rows = 3, cols = 3):
        self.rows = rows
        self.cols = cols
        self.state = {x: [[x for i in range(self.cols)] for j in range(self.rows)] for x in Cube.colors}
        print(self.state)

    def clockwise(self, face):
        new = deepcopy(self.state)
        # if face == w:
        #     for i in range(3):
        #         print(id(new[o][0][i]), id(new[o][1][i]))
        #         new[o][0][i] = self.state[g][i][2]
        #         new[g][i][2] = self.state[r][i][2]
        #         new[r][i][2] = self.state[b][0][i]
        #         new[b][0][i] = self.state[o][0][i]
        if face in Cube.colors:
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
            print(color_index_inOrder_ruld)
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

    def anticlockwise(self, face):
        new = deepcopy(self.state)
        # if face == w:
        #     for i in range(3):
        #         print(id(new[o][0][i]), id(new[o][1][i]))
        #         new[o][0][i] = self.state[g][i][2]
        #         new[g][i][2] = self.state[r][i][2]
        #         new[r][i][2] = self.state[b][0][i]
        #         new[b][0][i] = self.state[o][0][i]
        if face in Cube.colors:
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

    def apply(self, front, top, *formulas):
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
                    self.anticlockwise(di[formula[i]])
                    i += 2
                else:
                    self.clockwise(di[formula[i]])
                    i += 1
            if i == n:
                self.clockwise(di[formula[i]])

    def __str__(self):
        return str(self.state)

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


    def first_cross(self, first):
        done = []
        def color_on_top(self, first, i, j):
            if self.state[first][i][j] != first:
                raise ValueError
            otherSide = Cube.EotherSide(first, i, j)
            if otherSide[0] == self.state[otherSide[0]][otherSide[1]][otherSide[2]]:
                done.append(Cube.color2direction[first][otherSide[0]])
                return
            if len(done) > 0:
                

            pass
        def color_bottom(self):
            pass
        def color_side_top(self):
            pass
        def color_side_mid(self):
            pass
        def color_side_bottom(self):
            pass

    
    # def move(self, move):

c = Cube()
# c.apply(o, y, 'FRUR`U`RUR`U`RUR`U`F`')
# c.clockwise(g)
c.clockwise(w)
# c.anticlockwise(w)
# c.clockwise(w)
# print(c.otherSide(w, 1, 2))
# edge = set()
# opp = set()
# for color, mat in c.state.items():
#     for i, j in [(0,1), (1,0), (1, 2), (2,1)]:
#         x = (color, i, j)
#         edge.add(x)
#         y = c.otherSide(*x)
#         opp.add(y)
#         print(*x, ': ', y)
#         if x != c.otherSide(*y):
#             print("Something is wrong here")
            
print(c)
# if edge == opp:
#     print("Ya seems equal")