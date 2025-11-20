from core import Cube3x3, w, Moves
from solver3x3 import FirstCross, FirstCorners


def testFirstCross(*,numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False, getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    fails:list[dict[str,Moves]] = []
    passes:list[dict[str,Moves]]= []
    for _ in range(numberOfCases):
        c = Cube3x3()
        scram = c.apply_randomScramble(scrambleLimit)
        solver = FirstCross(c, w, True)
        moves = solver.solve_first_cross()
        if not solver.check_first_cross():
            fails.append(dict(scram=scram, moves=moves))
            if breakAtFirstFail:
                break
        elif len(passes) < getpasses:
            passes.append(dict(scram=scram, moves=moves))
    return dict(fails=fails, passes=passes)

def testFirstCorners(*,numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False, getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    fails:list[dict[str,Moves]] = []
    passes:list[dict[str,Moves]]= []
    for _ in range(numberOfCases):
        c = Cube3x3()
        scram = c.apply_randomScramble(scrambleLimit)
        solver = FirstCorners(c, w, True)
        moves = solver.solve_first_corners()
        if not solver.check_first_corners():
            fails.append(dict(scram=scram, moves=moves))
            if breakAtFirstFail:
                break
        elif len(passes) < getpasses:
            passes.append(dict(scram=scram, moves=moves))
    return dict(fails=fails, passes=passes)

