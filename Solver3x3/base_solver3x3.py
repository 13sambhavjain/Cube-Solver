from core import Cube3x3, FaceId, Color, Coords, back
from copy import deepcopy
class BaseSolver3x3():
    def __init__(self, cube: Cube3x3, 
                 start_faceid :FaceId=None, #type: ignore
                 change_original: bool=True) ->  None: 
        if not change_original:
            cube = deepcopy(cube)
        self.cube: Cube3x3 = cube
        self.start_faceid: FaceId = start_faceid if start_faceid else self.cube.start_faceId
        self.start_color: Color = Cube3x3.faceId2color(self.start_faceid)
        self.last_faceid: FaceId = Cube3x3.direction2faceId[self.start_faceid][back]

    def __getattr__(self, name):
        return self.cube.name
    
    def check_first_cross(self) -> bool:
        face = self.cube.state[self.start_faceid]
        for position in self.cube.edge_positions:
            if face.get(position) != self.start_color:
                return False
        return True
    
    def check_first_corners(self) -> bool:
        face = self.cube.state[self.start_faceid]
        for position in self.cube.corner_positions:
            if face.get(position) != self.start_color:
                return False
        return True
    
    def checkRaise_start_color_on_startface_coords(self, coords: Coords):
        if coords.face_id != self.start_faceid:
            raise ValueError("Coords are not on start face." + repr(coords))
        if self.cube.get(coords) != self.start_color:
            raise ValueError("At coords it is not start color." + repr(coords))
        
    def checkRaise_start_color_on_lastface_coords(self, coords: Coords):
        if coords.face_id != self.last_faceid:
            raise ValueError("Coords are not on last face." + repr(coords))
        if self.cube.get(coords) != self.start_color:
            raise ValueError("At coords it is not start color." + repr(coords))
    
    def checkRaise_start_color_on_sideface_coords(self, coords: Coords):
        if coords.face_id == self.start_faceid or coords.face_id == self.last_faceid:
            raise ValueError("Coords are not on last face." + repr(coords))
        if self.cube.get(coords) != self.start_color:
            raise ValueError("At coords it is not start color." + repr(coords))