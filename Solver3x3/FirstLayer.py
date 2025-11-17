from core import Cube3x3Statics, CubeMovements, Cube3x3, Cube, back, Position, Coords, FaceId, Move, Moves, Color
from copy import deepcopy

class FirstLayer():
    def __init__(self, cube: Cube3x3, change_original: bool=True) -> None:
        if not change_original:
            cube = deepcopy(cube)
        self.cube: Cube3x3 = cube
    
    def __getattr__(self, name):
        return self.cube.name
     
    def first_cross(self, start_faceid :FaceId=None) -> Moves: #type: ignore
        if start_faceid is None:
            start_faceid = self.cube.start_faceId
        start_color: Color = Cube3x3.faceId2color(start_faceid)
        placed_edge_colors = set()
        last_faceid = Cube.direction2faceId[start_faceid][back]
        def color_on_top(coords: Coords, check=True):
            if check:
                if coords.face_id != start_faceid:
                    raise ValueError("Coords are not on start face." + repr(coords))
                if self.cube.get(coords) != start_color:
                    raise ValueError("At coords it is not start color." + repr(coords))
                
            otherSide = Cube3x3.EdgeOtherSide(coords)
            otherColor = self.cube.get(otherSide)

            if Cube3x3.faceId2color(otherSide.face_id) == otherColor:
                placed_edge_colors.add(otherColor)
                return Moves(comment=f"{coords} is already placed.")
            
            if len(placed_edge_colors) == 0:
                # rotate color logic
                fromSide = Cube.faceId2direction[start_faceid][otherSide.face_id]
                toSide = Cube.faceId2direction[start_faceid][Cube3x3.color2faceId(otherColor)]
                moves = Moves([
                    Move(faceId=start_faceid, 
                        turns = Cube.side_directions.index(toSide) - Cube.side_directions.index(fromSide))
                            ])
                self.cube.apply_moves(moves)
                placed_edge_colors.add(otherColor)
                return moves
            else: 
                """ ***Improvement: some are already placed, but this is wrongly placed. should try to fit others first....Do this only if one more is stuck at wrong place, even when you do this should put it to side only not bottom."""
                new_coords = Cube3x3.BackEdgeCoords(coords)
                moves = Moves(
                    moves=[self.cube.double_rotate(otherSide.face_id)], 
                    comment=f"Putting the wrongply paced {start_color=} with the last color."
                ) + color_on_bottom(new_coords)
                return moves + color_on_bottom(new_coords)
        def color_on_bottom(coords: Coords, check=True):
            if check:
                if coords.face_id != last_faceid:
                    raise ValueError("Coords are not on last face." + repr(coords))
                if self.cube.get(coords) != start_color:
                    raise ValueError("At coords it is not start color." + repr(coords))

            otherSide = Cube3x3.EdgeOtherSide(coords)
            otherColor = self.cube.get(coords)
            fromSide = Cube.faceId2direction[last_faceid][otherSide.face_id]
            toSide = Cube.faceId2direction[last_faceid][Cube.color2faceId(otherColor)]
            placed_edge_colors.add(otherColor)
            moves =  Moves([Move(last_faceid, Cube.side_directions.index(toSide) - Cube.side_directions.index(fromSide)), Move(otherColor, 2)], comment=f"Placed {repr(coords)}")
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
    
