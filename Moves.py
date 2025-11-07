from Colors import Color, Colors, Face

class Move():
    def __init__(self, face: Face, turns: int=1):
        self.face: Face = face
        self._turns: int = turns%4
    
    @property
    def turns(self) -> int:
        return self._turns
    @turns.setter
    def turns(self, value: int):
        self._turns = value % 4
    
    def __str__(self) -> str:
        face_letter = self.face.name[0].upper()
        match self.turns:
            case 0:
                return ""
            case 1:
                return f'{face_letter}'
            case 2:
                return f'{face_letter}\u00b2'
            case 3:
                return f'{face_letter}`'
            case _:
                raise ValueError(f"Invalid number of turns, {self.__repr__()}")
    
    def __repr__(self):
        return f'{self.__class__.__name__}(face={self.face!r}, turns={self.turns!r})'
    
    def __bool__(self) -> bool:
        return self.turns != 0
    
    def __add__(self, other: Move) -> Move|Moves:
        if self.face == other.face:
            return Move(self.face, self.turns + other.turns)
        else:
            return Moves([self, other])
        
    def __radd__(self, other: Moves) -> Move|Moves:
        if not other:
            return self
        if self.face == other[0].face:
            return Move(self.face, self.turns + sum(move.turns for move in other))
        return Moves([self] + other)

class Moves():
    def __init__(self, moves: list[Move]):
        self.moves: list[Move] = moves
    
    def __str__(self) -> str:
        return ' '.join(str(move) for move in self.moves)
    
    def __repr__(self):
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})'
    
    def append(self, move: Move):
        if not move:
            return
        if self.moves and self.moves[-1].face == move.face:
            combined_turns = (self.moves[-1].turns + move.turns) % 4
            if combined_turns == 0:
                self.moves.pop()
            else:
                self.moves[-1].turns = combined_turns
        else:
            self.moves.append(move)
    
    def pop(self) -> Move:
        return self.moves.pop()
    
    def __len__(self) -> int:
        return len(self.moves)
    
    def __getitem__(self, index: int) -> Move:
        return self.moves[index]
    
    def __iter__(self):
        return iter(self.moves)
    
    def __repr__(self):
        return f'Moves(moves={self.moves})'
    
    def extend(self, moves: list[Move]):
        for move in moves:
            self.append(move)

    def __setitem__(self, index: int, move: Move):
        self.moves[index] = move

    def __contains__(self, move: Move) -> bool:
        return move in self.moves
    
    def __bool__(self) -> bool:
        return bool(self.moves)
    
    def __add__(self, other: Move|Moves) -> Moves:
        result = Moves(self.moves.copy())
        if isinstance(other, Move):
            result.append(other)
        elif isinstance(other, Moves):
            for move in other:
                result.append(move)
        return result