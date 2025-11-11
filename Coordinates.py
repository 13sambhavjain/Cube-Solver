from Face import FaceId

class Position():
    """Postion on a Face"""
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __getitem__(self, index: int) -> int:
        index %= 2
        if index==1:
            return self.y
        return self.x

    def __setitem__(self, index: int, value: int) -> None:
        index %= 2
        if index==1:
            self.y = value
        else:
            self.x = value
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})'    
    
class Coords():
    # """Coordinates of a Color in a Cube with fix center"""
    def __init__(self, face_id: FaceId, x: int, y: int):
        self.face_id: FaceId = face_id
        self.pos: Position = Position(x, y)

    @property
    def x(self) -> int:
        return self.pos.x
    @x.setter
    def x(self, value: int):
        self.pos.x = value

    @property
    def y(self) -> int:
        return self.pos.y
    @y.setter
    def y(self, value: int):
        self.pos.y = value

    def __iter__(self):
        yield self.face_id
        yield self.x
        yield self.y

    def __getitem__(self, index: int) -> FaceId|int:
        index %= 3
        if index == 0:
            return self.face_id
        elif index == 1:
            return self.x
        else: # index == 2
            return self.y

    def __setitem__(self, index: int, value: FaceId|int) -> None:
        index %= 3
        if index == 0:
            self.face_id = value # type: ignore
        elif index == 1:
            self.x = value # type: ignore
        else: # index == 2
            self.y = value # type: ignore

    def __str__(self) -> str:
        return f'({self.face_id}, {self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})'
    
