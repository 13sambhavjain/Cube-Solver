from enum import StrEnum, auto

class Direction(StrEnum):
    front = auto()
    back = auto()
    left = auto()
    right = auto()
    up = auto()
    down = auto()

class SideDirections():
    """A collection of Side Directions with cyclic indexing and iteration."""
    _sideDirections = [Direction.up, Direction.right, Direction.down, Direction.left]
    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance of SideDirections exists."""
        if cls._instance is None:
            cls._instance = super(SideDirections, cls).__new__(cls)
        return cls._instance
    
    def __iter__(self):
        """Allow iteration: for direction in SideDirections"""
        return iter(self._sideDirections)

    def __getitem__(self, index: int) -> Direction:
        """Allow cyclic indexing: sideDirections[n] wraps around."""
        return self._sideDirections[index % len(self._sideDirections)]
    
    def __contains__(self, direction: Direction) -> bool:
        """Check if a direction is a side direction."""
        return direction in self._sideDirections

    def __len__(self) -> int:
        """Number of side directions."""
        return len(self._sideDirections)

    def index(self, direction: Direction) -> int:
        """Return the index of a given direction."""
        return self._sideDirections.index(direction)

    def next(self, direction: Direction) -> Direction:
        """Return the next side direction cyclically."""
        i = self._sideDirections.index(direction)
        if i == -1:
            raise ValueError(f"{direction} not in SideDirections")
        return self._sideDirections[(i + 1) % len(self._sideDirections)]

    def prev(self, direction: Direction) -> Direction:
        """Return the previous side direction cyclically."""
        i = self._sideDirections.index(direction)
        if i == -1:
            raise ValueError(f"{direction} not in SideDirections")
        return self._sideDirections[(i - 1) % len(self._sideDirections)]

    def __str__(self):
        """String representation of the SideDirections collection."""
        return f"SideDirections({', '.join(c.name for c in self._sideDirections)})"
    
    def __repr__(self):
        """Official string representation of the SideDirections collection."""
        return f'SideDirections(_sideDirections={self._sideDirections}, _instance={object.__repr__(self._instance) if self._instance else None})'


if __name__ == "__main__":
    # colors = SideDirections()
    # print(colors[0])
    # for color in colors:
    #     print(color)
    # print(colors.next(Direction.right))
    # print(colors.prev(Direction.up))
    # print(colors.index(Direction.down))
    # print(len(colors))
    # print(colors.__repr__())
    pass