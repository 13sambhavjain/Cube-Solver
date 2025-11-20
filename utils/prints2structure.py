from core import Cube3x3
from core import Colors
def print2Cube3x3(printed_cube3x3: str) -> Cube3x3:
    """function to convert a unformated print of Cube3x3 to a Cube3x3"""
    lines = [k for line in printed_cube3x3.split('\n') if (k:=line.rstrip().lstrip().split())]
    i2color = dict()
    for color in Colors():
        i2color[f'{color:i}'.strip()] = color
    state

    return Cube3x3()
