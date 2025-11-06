from Colors import Color
import copy, warnings

class Face:
    def __init__(self, size: int=3, faceCenter: Color = None, grid: list[list[Color]] = None):
        """Initializes a Face object. Requires either a faceCenter color (to generate a new grid)
        OR an existing grid to load from."""
        #Validation and Warnings---
        if (faceCenter is None) == (grid is None):
            # If neither OR both are None
            if faceCenter is not None: # Means both are NOT None (both are provided)
                 warnings.warn(..., stacklevel=2) # Warning case
            else: # Means both ARE None (neither provided)
                 raise ValueError(...) # Error case
        
        # Initialization Logic uses grid on higher priority---
        if grid is not None:
            self.grid = copy.deepcopy(grid)
        else:
            self.grid = [[faceCenter for _ in range(size)] for _ in range(size)]
            
        self._size = size
            

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value) -> AttributeError:
        raise AttributeError('Face.size attribute is not ment to change once the Face is created.')

    def __str__(self) -> str:
        return '\n'.join(' '.join(cell.name[0].upper() for cell in row) for row in self.grid)
    
    def __format__(self, format_spec: str) -> str:
        """
        Custom formatting for the Face grid output using comprehensions.
        - 's' or '': Single letter representation (default).
        - 'a': ANSI colored boxes representation.
        - 'i': returns the ANSI background code with initials in them
        """
        # Use the format() function dynamically
        if not format_spec:
            return str(self)
        return '\n'.join(
            "".join(format(cell, format_spec) for cell in row) 
            for row in self.grid
        )
        
    
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
        """
        Reversible representation assuming standard construction.
        """
        # We output faceCenter and size, matching the constructor signature.
        # We omit grid as it's generated automatically by __init__.
        return f'{self.__class__.__name__}'
    
class Position():
    """Postion on a Face"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __getitem__(self, index: int) -> int:
        index %= 2
        if index==1:
            return self.y
        return self.x
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})'    
    
class Coord():
    """Coordinates of a Color in a Cube with fix center"""
    def __init__(self, faceCenter: Color, x: int, y: int):
        self.faceCenter = faceCenter
        self.pos = Position(x, y)

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

    def __getitem__(self, index: int) -> int:
        index %= 3
        match index:
            case 0:
                return self.faceCenter
            case 1:
                return self.x
            case 2:
                return self.y
        raise Exception(f'For unknown reason match case failed here. {self.__repr__()}')

    def __str__(self) -> str:
        return f'({self.faceCenter}, {self.x}, {self.y})'

    def __repr__(self):
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})'
    


if __name__ == "__main__":
    # print(Coord(Color.white, 1, 2).__repr__())
    # print(Position( 1, 2).__repr__())

    print(f'{Face(3, Color.white)}')
        
    
