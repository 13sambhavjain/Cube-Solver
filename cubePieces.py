from Colors import *
class Color:
    def __init__(self, color: str, neighbours: list = None):
        self.color = color
        self.neighbours = neighbours

    # def replace(self, neigh_new, neigh_old):
    #     self

class Center:
    def __init__(self, color: str, neighbours: list = None):
        self.colors = [Color(color, neighbours)]

class Edge:
    def __init__(self, color1: str, color2: str, neighbours1: list = None, neighbours2: list = None):
        self.colors = [Color(color1, neighbours1), Color(color2, neighbours2)]

class Corner:
    def __init__(self, color1: str, color2: str, color3: str, neighbours1: list = None, neighbours2: list = None, neighbour3: list = None):
        self.colors = [Color(color1, neighbours1), Color(color2, neighbours2), Color(color3, neighbour3)]

class Cube:
    colors = [w,b,o,y,g,r]
    def __init__(self):
        self.centers = [Center(c) for c in Cube.colors]
        self.edges = [Edge(w, b), Edge(w, o), Edge(w, g), Edge(w, r), Edge(b, o), Edge(o, g), Edge(g, r), Edge(r, b), Edge(y, b), Edge(y, o), Edge(y, g), Edge(y, r)]
        self.corners = [Corner(w, b, o), Corner(w, o, g), Corner(w, g, r), Corner(w, r, b), Corner(y, b, o), Corner(y, o, g), Corner(y, g, r), Corner(y, r, b)]

