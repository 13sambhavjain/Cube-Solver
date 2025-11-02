from enum import StrEnum, auto

class Direction(StrEnum):
    front = auto()
    back = auto()
    left = auto()
    right = auto()
    up = auto()
    down = auto()

class SideDirections():
    _sideDirections = [Direction.up, Direction.right, Direction.down, Direction.left]
    def __iter__(self):
        """Allow iteration: for direction in SideDirections"""
        return iter(self._sideDirections)

    def __getitem__(self, index: int) -> Direction:
        """Allow cyclic indexing: Colors[n] wraps around."""
        return self._colors[index % len(self._sideDirections)]
    
    def __contains__(self, direction: Direction) -> bool:
        return direction in self._sideDirections

    def __len__(self):
        """Number of colors."""
        return len(self._sideDirections)

    def index(self, direction: Direction) -> int:
        """Return the index of a given color."""
        return self._sideDirections.index(direction)

    def next(self, direction: Direction) -> Direction:
        """Return the next color cyclically."""
        i = self.index(direction)
        return self[(i + 1) % len(self)]

    def prev(self, direction: Direction) -> Direction:
        """Return the previous color cyclically."""
        i = self.index(direction)
        return self[(i - 1) % len(self)]

    def __repr__(self):
        return f"Colors({', '.join(c.name for c in self._sideDirections)})"
