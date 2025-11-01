from enum import StrEnum, auto

class Color(StrEnum):
    red = auto()
    blue = auto()
    green = auto()
    yellow = auto()
    white = auto()
    orange = auto()

class Direction(StrEnum):
    front = auto()
    back = auto()
    left = auto()
    right = auto()
    up = auto()
    down = auto()

Face = Color

class Move():
    def __init__(self, face: Face, numberOfturns: int=1):
        self.face: Face = face
        self.turns: int = numberOfturns%4
        
    def __str__(self) -> str:
        face_letter = self.face.name[0].upper()
        match self.turns:
            case 0:
                return ""
            case 1:
                return f'{face_letter}'
            case 2:
                return f'{face_letter}\u00b2'
            case 3:
                return f'{face_letter}`'
            case _:
                self.turns %= 4
                return self.__str__()
    
    def __repr__(self):
        return f'Move(face={self.face}, turns={self.turns})'


w = Color.white
b = Color.blue
y = Color.yellow
g = Color.green
o = Color.orange
r = Color.red

right = Direction.right
left = Direction.left
up = Direction.up
down = Direction.down
opp = Direction.back

m = Move(w)
print(m)

# w = 'white
# b = 'blue'
# g = 'green'
# y = 'yellow'
# o = 'orange'
# r = 'red'
# right = 'right'
# up = 'up'
# down = 'down'
# left = 'left'
# opp = 'opp'


# __all__ = [getattr(Color, name) for name in Color.__members__]

# print(__all__)