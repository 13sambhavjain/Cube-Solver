from Colors import Color
import copy, warnings

class Face:
    def __init__(self, size: int=3, fill_color: Color = None, grid: list[list[Color]] = None):
        """Initializes a Face object. Requires either a fill_color color (to generate a new grid)
        OR an existing grid to load from."""
        #Validation and Warnings---
        if (fill_color is None) == (grid is None):
            # If neither OR both are None
            if fill_color is not None: # Means both are NOT None (both are provided)
                warnings.warn("Both fill_color and grid are provided. Using grid.",UserWarning, stacklevel=2) # Warning case
            else: # Means both ARE None (neither provided)
                raise ValueError("Either fill_color or grid must be provided.") # Error case

        # Initialization Logic uses grid on higher priority---
        if grid is not None:
            self.grid = copy.deepcopy(grid)
        else:
            self.grid = [[fill_color for _ in range(size)] for _ in range(size)]
            
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
        first_color: Color = self.grid[0][0]
        return all(first_color == color for row in self.grid for color in row)
    
    def __bool__(self) -> bool:
        return bool(self.grid)
    
    def __repr__(self) -> str:
        """
        Reversible representation assuming standard construction.
        """
        # We output fill_color and size, matching the constructor signature.
        # We omit grid as it's generated automatically by __init__.
        return f'{self.__class__.__name__}(size={self.size!r}, grid={self.grid!r})'
    
FaceId = Color
    
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
            self.face_id = value
        elif index == 1:
            self.x = value
        else: # index == 2
            self.y = value
        
    def __str__(self) -> str:
        return f'({self.face_id}, {self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})'
    


if __name__ == "__main__":
    # print(Coord(Color.white, 1, 2).__repr__())
    # print(Position( 1, 2).__repr__())

    print(f'{Face(3, Color.white)}')
        
    
