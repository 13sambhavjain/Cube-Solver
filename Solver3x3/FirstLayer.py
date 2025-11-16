from core import Cube3x3Statics, CubeMovements, Cube3x3, Cube, back, Position, Coords
from copy import deepcopy

class FirstLayer():
    def __init__(self, cube: Cube3x3, change_original: bool=True) -> None:
        if not change_original:
            cube = deepcopy(cube)
        self.cube: Cube3x3 = cube
    
    def __getattr__(self, name):
        return self.cube.name
     
    def first_cross(self, start_faceid=None):
        if start_faceid == None:
            start_faceid = self.cube.start_faceId
        placed_egde_colors = set()
        last_faceid = self.cube.direction2faceId[start_faceid][back]


        def color_on_top(pos: Position):
            if self.state[start_faceid].get(pos) != start_faceid:
                raise ValueError
            otherSide = Cube3x3.EdgeOtherSide(Coords(start_faceid, pos.x, pos.y))
            otherColor = self.state[otherSide[0]][][]
            if otherSide[0] == otherColor:
        def color_on_top(pos: Position):
            if self.state[start_faceid].get(pos) != start_faceid:
                raise ValueError
            otherSide = Cube3x3.EdgeOtherSide(Coords(start_faceid, pos.x, pos.y))
            otherColor = self.state[otherSide[0]][][]
            if otherSide[0] == otherColor:
                placed_egde_colors.add(otherColor)
                return list()
            if len(placed_egde_colors) == 0:
                # rotate color logic
                fromSide = Cube.faceId2direction[start_faceid][otherSide[0]]
                toSide = Cube.faceId2direction[start_faceid][otherColor]
                placed_egde_colors.add(otherColor)
                return [self.clockwise(start_faceid, Cube.side_directions.index(toSide) - Cube.side_directions.index(fromSide))]
            else:
                moves = [self.clockwise(otherSide[0], 2)] 
                li, lj = Cube.BackEdgeCoords(i, j)
                if self.state[last_faceid][li][lj] != start_faceid:
                    raise Exception
                return moves + color_on_bottom(li, lj)
        def color_on_bottom(i, j):
            otherSide = self.EotherSide(last_faceid, i, j)
            otherColor = self.state[otherSide[0]][otherSide[1]][otherSide[2]]
            fromSide = Cube.faceId2direction[last_faceid][otherSide[0]]
            toSide = Cube.faceId2direction[last_faceid][otherColor]
            placed_egde_colors.add(otherColor)
            return [self.clockwise(last_faceid, Cube.side_directions.index(toSide) - Cube.side_directions.index(fromSide)), self.clockwise(otherColor, 2)]
        
        def color_on_side(coords: Coords):
            otherSide = self.EdgeOtherSide(coords)
            otherColor = self.state[otherSide[0]][otherSide[1]][otherSide[2]]
            def color_on_side_top():
                fromSide = Cube.faceId2direction[start_faceid][c]
                toSide = Cube.faceId2direction[start_faceid][otherColor]
                rotate = (Cube.side_directions.index(toSide) - Cube.side_directions.index(fromSide))
                rotate %= 4 # rotating first for fromSide to reach toSide
                placed_egde_colors.add(otherColor)
                if rotate == 3:
                    return self.apply(c,start_faceid, 'FR')
                if rotate == 2:
                    return self.apply(c,start_faceid, 'FURU`')
                if rotate == 1:
                    return self.apply(c,start_faceid, 'F`L`')
                if rotate == 0:
                    return self.apply(c,start_faceid, 'FU`RU')
            def color_on_side_mid():
                fromSide = Cube.faceId2direction[start_faceid][otherColor]
                toSide = Cube.faceId2direction[start_faceid][otherSide[0]]
                r1 = (Cube.side_directions.index(toSide) - Cube.side_directions.index(fromSide))
                otherFrom = Cube.faceId2direction[otherSide[0]][c]
                otherTo = Cube.faceId2direction[otherSide[0]][start_faceid]
                r2 = (Cube.side_directions.index(otherTo) - Cube.side_directions.index(otherFrom))
                placed_egde_colors.add(otherColor)
                return [self.clockwise(start_faceid, r1), self.clockwise(otherSide[0], r2), self.anticlockwise(start_faceid, r1)]
            def color_on_side_bottom():
                # fromSide = Cube.faceId2direction[first][otherColor]
                moves = None
                if otherColor == c:
                    return self.apply(c, start_faceid, 'F`U`RU')
                if otherColor == Cube.direction2color[c][opp]:
                    moves = self.apply(c, start_faceid, 'F`URU`')
                    if c in placed_egde_colors:
                        moves.append(self.clockwise(c))
                    return moves
                fromSide = Cube.faceId2direction[c][last_faceid]
                toSide = Cube.faceId2direction[c][otherColor]
                rotate = (Cube.side_directions.index(toSide) - Cube.side_directions.index(fromSide))%4
                fromSide1 = Cube.faceId2direction[otherColor][c]
                toSide1 = Cube.faceId2direction[otherColor][start_faceid]
                rotate1 = (Cube.side_directions.index(toSide1) - Cube.side_directions.index(fromSide1))%4
                moves = [
                    self.clockwise(c, rotate),
                    self.clockwise(otherColor, rotate1)
                ]
                if c in placed_egde_colors:
                    moves.append(self.anticlockwise(c, rotate)) #changed from clock - to - anticlock
                placed_egde_colors.add(otherColor)
                return moves

            if otherSide[0] == start_faceid:
                return color_on_side_top()
            elif otherSide[0] == last_faceid:
                return color_on_side_bottom()
            else:
                return color_on_side_mid()
        # while len(done) < 4:
        cross_moves = list()
        while(len(placed_egde_colors) < 4):
            for c in self.state:
                for i in range(3):
                    for j in range(3):
                        if (i+j)&1 and self.state[c][i][j] == start_faceid:
                            if c == start_faceid:
                                cross_moves += color_on_top(i, j)
                            elif c == last_faceid:
                                cross_moves += color_on_bottom(i,j)
                            else:
                                cross_moves += color_on_side(c, i, j)

        return cross_moves
    
