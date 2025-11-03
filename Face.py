from Colors import Color

class Face:
    def __init__(self, color: Color, n=3):
        self._n : int= n
        self.grid: list[list[Color]] = [[color for _ in range(n)] for _ in range(n)]

    def __str__(self) -> str:
        return '\n'.join(' '.join(cell.name[0].upper() for cell in row) for row in self.grid)
    
    def rotate_clockwise(self) -> None:
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def rotate_anticlockwise(self) -> None:
        self.grid = [list(row) for row in zip(*self.grid)][::-1]

    def __iter__(self):
        return iter(self.grid)
    
    def __getitem__(self, index:int) -> list[Color]:
        return self.grid[index]
    
    def __setitem__(self, index: int, value: list[Color]) -> None:
        self.grid[index] = value
    
    def __contains__(self, color: Color) -> bool:
        if isinstance(color, Color):
            for row in self.grid:
                if row.__contains__(color):
                    return True
            return False
        else:
            return self.grid.__contains__(color)
    
    def solved(self) -> bool:
        if self:
            first_color: Color = self.grid[0][0]
            return all(first_color == color for row in self.grid for color in row)
        raise ValueError(f'Face doesn\'t exist. {self.__repr__()}')
    
    def __bool__(self) -> bool:
        return bool(self.grid)
    
    def __repr__(self) -> str:
        return f'Face(n={self._n}, grid={self.grid})'
    

        
    
        
    
