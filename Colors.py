from enum import StrEnum, auto

class Color(StrEnum):
    white = auto()
    blue = auto()
    orange = auto()
    yellow = auto()
    green = auto()
    red = auto()

class Colors():
    _colors = list(Color)
    def __iter__(self):
        """Allow iteration: for color in Colors"""
        return iter(self._colors)

    def __getitem__(self, index: int) -> Color:
        """Allow cyclic indexing: Colors[n] wraps around."""
        return self._colors[index % len(self._colors)]
    
    def __contains__(self, color: Color) -> bool:
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
        return f"Colors({', '.join(c.name for c in self._colors)})"


Face = Color

