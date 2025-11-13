from core import Cube3x3Statics, CubeMovements, Cube3x3, Cube, back

class FirstLayer():
    def __init__(self, cube: Cube3x3) -> None:
        self.cube: Cube3x3 = cube
    
    def __getattribute__(self, name):
        return self.cube.name
    

    def first_cross(self, first_faceid=self.cube.):
        # self = deepcopy(demoself)
        done = set()
        last = Cube.direction2color[first_faceid][back]
        def color_on_top(i, j):
            if self.state[first_faceid][i][j] != first_faceid:
                raise ValueError
            otherSide = Cube.EotherSide(first_faceid, i, j)
            otherColor = self.state[otherSide[0]][otherSide[1]][otherSide[2]]
            if otherSide[0] == otherColor:
                done.add(otherColor)
                return list()
            if len(done) == 0:
                # rotate color logic
                fromSide = Cube.color2direction[first_faceid][otherSide[0]]
                toSide = Cube.color2direction[first_faceid][otherColor]
                done.add(otherColor)
                return [self.clockwise(first_faceid, Cube.directions.index(toSide) - Cube.directions.index(fromSide))]
            else:
                moves = [self.clockwise(otherSide[0], 2)] 
                li, lj = Cube.OppositeEdgeCoords(i, j)
                if self.state[last][li][lj] != first_faceid:
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
                fromSide = Cube.color2direction[first_faceid][c]
                toSide = Cube.color2direction[first_faceid][otherColor]
                rotate = (Cube.directions.index(toSide) - Cube.directions.index(fromSide))
                rotate %= 4 # rotating first for fromSide to reach toSide
                done.add(otherColor)
                if rotate == 3:
                    return self.apply(c,first_faceid, 'FR')
                if rotate == 2:
                    return self.apply(c,first_faceid, 'FURU`')
                if rotate == 1:
                    return self.apply(c,first_faceid, 'F`L`')
                if rotate == 0:
                    return self.apply(c,first_faceid, 'FU`RU')
            def color_on_side_mid():
                fromSide = Cube.color2direction[first_faceid][otherColor]
                toSide = Cube.color2direction[first_faceid][otherSide[0]]
                r1 = (Cube.directions.index(toSide) - Cube.directions.index(fromSide))
                otherFrom = Cube.color2direction[otherSide[0]][c]
                otherTo = Cube.color2direction[otherSide[0]][first_faceid]
                r2 = (Cube.directions.index(otherTo) - Cube.directions.index(otherFrom))
                done.add(otherColor)
                return [self.clockwise(first_faceid, r1), self.clockwise(otherSide[0], r2), self.anticlockwise(first_faceid, r1)]
            def color_on_side_bottom():
                # fromSide = Cube.color2direction[first][otherColor]
                moves = None
                if otherColor == c:
                    return self.apply(c, first_faceid, 'F`U`RU')
                if otherColor == Cube.direction2color[c][opp]:
                    moves = self.apply(c, first_faceid, 'F`URU`')
                    if c in done:
                        moves.append(self.clockwise(c))
                    return moves
                fromSide = Cube.color2direction[c][last]
                toSide = Cube.color2direction[c][otherColor]
                rotate = (Cube.directions.index(toSide) - Cube.directions.index(fromSide))%4
                fromSide1 = Cube.color2direction[otherColor][c]
                toSide1 = Cube.color2direction[otherColor][first_faceid]
                rotate1 = (Cube.directions.index(toSide1) - Cube.directions.index(fromSide1))%4
                moves = [
                    self.clockwise(c, rotate),
                    self.clockwise(otherColor, rotate1)
                ]
                if c in done:
                    moves.append(self.anticlockwise(c, rotate)) #changed from clock - to - anticlock
                done.add(otherColor)
                return moves

            if otherSide[0] == first_faceid:
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
                        if (i+j)&1 and self.state[c][i][j] == first_faceid:
                            if c == first_faceid:
                                cross_moves += color_on_top(i, j)
                            elif c == last:
                                cross_moves += color_on_bottom(i,j)
                            else:
                                cross_moves += color_on_side(c, i, j)

        return cross_moves
    
