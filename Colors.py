from enum import StrEnum, auto

class Color(StrEnum):
    white = auto()
    blue = auto()
    orange = auto()
    yellow = auto()
    green = auto()
    red = auto()

class Colors():
    """A collection of Colors with cyclic indexing and iteration."""
    _colors = [Color.white, Color.blue, Color.orange, Color.yellow, Color.green, Color.red]
    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance of Colors exists."""
        if cls._instance is None:
            cls._instance = super(Colors, cls).__new__(cls)
        return cls._instance

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
        return f'Colors(_colors={self._colors}, _instance={object.__repr__(self._instance) if self._instance else None})'

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
    pass