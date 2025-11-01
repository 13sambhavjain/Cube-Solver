from enum import global_enum, StrEnum, auto

class Color(StrEnum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    WHITE = auto()
    ORANGE = auto()

w = 'white'
b = 'blue'
g = 'green'
y = 'yellow'
o = 'orange'
r = 'red'
right = 'right'
up = 'up'
down = 'down'
left = 'left'
opp = 'opp'

# __all__ = [getattr(Color, name) for name in Color.__members__]

# print(__all__)