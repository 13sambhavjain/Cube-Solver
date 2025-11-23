from . import BaseSolver3x3
from core import Cube3x3, up, Coords, FaceId, Move, Moves, Color, Position, down, left, Direction, front, back
from .solving_algos import Algo
from functools import cache
class LastLayer(BaseSolver3x3):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.side_faceids: list[FaceId] = list(
            map(lambda side_direction: Cube3x3.direction2faceId[self.start_faceid][side_direction],
                Cube3x3.side_directions)
        )
        self.connecting_side_face_coords: dict[FaceId, list[Coords]] = {
            faceid:  self.connectingCoords_withlastface(faceid) for faceid in self.side_faceids
        }
        self.last_face = self.cube.state[self.last_faceid]
        self.front_faceid = Color.green
    
    def prev_faceid(self, faceid: FaceId) -> FaceId:
        rotate = Cube3x3.side_directions.index(Cube3x3.faceId2direction[faceid][self.last_faceid])
        return Cube3x3.direction2faceId[faceid][Cube3x3.side_directions[(rotate+1)%4]]

    def back_faceid(self, faceid: FaceId) -> FaceId:
        return Cube3x3.direction2faceId[faceid][back]

    @cache
    def connectingCoords_withlastface(self, faceid: FaceId) -> list[Coords]:
        pos: Position= Cube3x3.sideDirection2edgePosition[Cube3x3.faceId2direction[faceid][self.last_faceid]]
        if pos.x&1:
            return [Coords(faceid, x = x, y=pos.y) for x in range(self.cube.size)]
        else:
            return [Coords(faceid, x=pos.x, y=y) for y in range(self.cube.size)]
    
    # def dot2cross(self):
    #     front = self.side_faceids[0] #random doesn't matter
    #     formula = self.cross_formula1*2 +'U' + self.cross_formula1
    #     moves = self.cube.apply_formula(front, self.last_faceid, formula)
    #     moves.comment = f"Dot before yellow Cross: {formula}"
    #     return moves
    def apply_algo(self, front: FaceId, algo: Algo) -> Moves:
        moves = self.cube.apply_formula(front, self.last_faceid, algo)
        moves.comment = f"Appling Algo ({algo.name}: {algo.value}) from FaceId: {front}."
        return moves
    
    def solve_OLL_edges(self) -> Moves:
        cross_yellow_pos: list[Position] = []
        for pos in  Cube3x3.edge_positions:
            if self.last_face.get(pos) == self.last_color:
                cross_yellow_pos.append(pos)
        if len(cross_yellow_pos) == 0:
            return self.apply_algo(self.side_faceids[0], Algo.OLL.Edges.dot_shape)
        elif len(cross_yellow_pos) == 4:
            return Moves([], comment="OLL of edges already done.")
        elif len(cross_yellow_pos) == 2:
            if cross_yellow_pos[0].x == cross_yellow_pos[1].x:
                return self.apply_algo(Cube3x3.direction2faceId[self.last_faceid][down], Algo.OLL.Edges.I_shape)
            elif cross_yellow_pos[0].y == cross_yellow_pos[1].y:
                return self.apply_algo(Cube3x3.direction2faceId[self.last_faceid][left], Algo.OLL.Edges.I_shape)
            else: 
                # due to order of appending in cross_yellow_pos
                if cross_yellow_pos[0] == Position(0,1) and cross_yellow_pos[1] == Position(1,0):
                    cross_yellow_pos.reverse()
                return self.apply_algo(
                    Cube3x3.EdgeOtherSide(Coords(self.last_faceid, pos=cross_yellow_pos[1])).face_id,
                    Algo.OLL.Edges.L_shape
                )
        raise NotImplementedError
    
    def solve_OLL_corners(self):
        side_face_with_lastcolor: dict[FaceId, Coords] = dict()
        for faceid, side_coords in self.connecting_side_face_coords.items():
            sfl = side_face_with_lastcolor[faceid] = list()
            for coords in (side_coords[0], side_coords[-1]):
                if self.cube.get(coords) == self.last_color:
                    sfl.append(coords)
        lastcolor_count2faceidlist: list[list[FaceId]] = [[],[],[]]
        for faceid, color_coords in side_face_with_lastcolor.items():
            lastcolor_count2faceidlist[len(color_coords)].append(faceid)
        if lastcolor_count2faceidlist[2]:
            if len(lastcolor_count2faceidlist[2]) == 2:
                # headlight taillight case
                return self.apply_algo(
                    lastcolor_count2faceidlist[0][0], 
                    Algo.OLL.Corners.H
                )
            else:
                if len(lastcolor_count2faceidlist[1]) == 0:
                    # just headlights
                    return self.apply_algo(
                        lastcolor_count2faceidlist[2][0], 
                        Algo.OLL.Corners.U
                    )
                else: #== 2
                    # headlight side light case
                    return self.apply_algo(
                        self.prev_faceid(lastcolor_count2faceidlist[2][0]), 
                        Algo.OLL.Corners.Pi
                    )
        elif lastcolor_count2faceidlist[1]:
            if lastcolor_count2faceidlist[1] == 3:
                if self.cube.get(self.connectingCoords_withlastface(lastcolor_count2faceidlist[1][0])[0]) == self.last_color:
                    # Sune
                    return self.apply_algo(
                        self.prev_faceid(lastcolor_count2faceidlist[0][0]), 
                        Algo.OLL.Corners.Sune
                    )
                else:
                    # AntiSune
                    return self.apply_algo(
                        Cube3x3.direction2faceId[lastcolor_count2faceidlist[0][0]][back], 
                        Algo.OLL.Corners.Sune
                    )
                


        else:
            return Moves([], comment="OLL of corners already done.")


                

            


        


