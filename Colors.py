from enum import StrEnum, auto

_COLOR_ANSI_MAP = {
    'white':  '\033[47m', 
    'blue':   '\033[44m',
    'orange': '\033[48;5;208m',
    'yellow': '\033[43m',
    'green':  '\033[42m',
    'red':    '\033[41m',
}
_RESET_CODE = '\033[0m'

class Color(StrEnum):
    white = auto()
    blue = auto()
    orange = auto()
    yellow = auto()
    green = auto()
    red = auto()

    @classmethod
    def get_reset_code(cls):
        return _RESET_CODE

    def __format__(self, format_spec: str):
        """
        Custom formatting using format specifiers:
        - 's': returns the color name
        - 'a': returns the ANSI background code + reset code
        - 'i': returns the ANSI background code + initial letter + reset code
        """
        if format_spec == 'i':
            # Returns background code + initial letter + RESET
            return f"{_COLOR_ANSI_MAP[self.name]}{self.name[0].upper():^3}{_RESET_CODE}"
        elif format_spec == 'a':
            # Returns just the background code + two spaces + RESET
            return f"{_COLOR_ANSI_MAP[self.name]}  {_RESET_CODE}"
        elif format_spec == 's' or format_spec == '':
            return str(self)
        else:
            return format(str(self), format_spec)

    def __repr__(self):
        # Returns a string that looks like "Color.<ColorName>"
        return f"{self.__class__.__name__}.{self.name}"

class Colors():
    """A collection of Colors with cyclic indexing and iteration."""
    _colors = [Color.white, Color.blue, Color.orange, Color.yellow, Color.green, Color.red]
    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance of Colors exists."""
        if cls._instance is None:
            cls._instance = super(Colors, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, *args, **kwargs):
        """
        Flexible initializer that accepts any arguments.
        It doesn't actually use args/kwargs for anything in this specific setup,
        but it makes the class definition resilient to being called with arguments.
        """
        pass

    def __iter__(self):
        """Allow iteration: for color in Colors"""
        return iter(self._colors)

    def __getitem__(self, index: int) -> Color:
        """Allow cyclic indexing: Colors[n] wraps around."""
        return self._colors[index % len(self._colors)]
    
    def __contains__(self, color: Color) -> bool:
        """Check if a color is in the collection."""
        return color in self._colors

    def __len__(self):
        """Number of colors."""
        return len(self._colors)

    def index(self, color: Color) -> int:
        """Return the index of a given color."""
        return self._colors.index(color)

    def next(self, color: Color) -> Color:
        """Return the next color cyclically."""
        i = self.index(color)
        return self[(i + 1) % len(self)]

    def prev(self, color: Color) -> Color:
        """Return the previous color cyclically."""
        i = self.index(color)
        return self[(i - 1) % len(self)]
    
    def __repr__(self):
        """Official string representation of the Colors collection."""
        return f'Colors(_colors={self._colors})'

    def __str__(self):
        """String representation of the Colors collection."""
        return f"Colors({', '.join(c.name for c in self._colors)})"
    

if __name__ == "__main__":
    # colors = Colors()
    # print(colors[0])
    # for color in colors:
    #     print(color)
    # print(colors.next(Color.red))
    # print(colors.prev(Color.white))
    # print(colors.index(Color.green))
    # print(len(colors))
    # print(colors.__repr__())
    print(Color.white.__repr__())
    pass