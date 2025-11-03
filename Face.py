from Colors import Color

class Face:
    def __init__(self, color: Color, n=3):
        self.n = n
        self.grid = [[color for _ in range(n)] for _ in range(n)]

    def __str__(self):
        return '\n'.join(' '.join(cell.name[0].upper() for cell in row) for row in self.grid)
    
    # def rotate_clockwise(self):
    #     self.grid = [list(row) for row in zip(*self.grid[::-1])]

    # def rotate_anticlockwise(self):
    #     self.grid = [list(row) for row in zip(*self.grid)][::-1]
