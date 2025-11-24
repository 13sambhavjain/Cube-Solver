from core import Cube3x3, w, Moves
from solver3x3 import *
from typing import Callable
import random

def test(solver_class: type[object], func: Callable, check_func: Callable,
        numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False,
        getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    fails:list[dict[str,Moves]] = []
    passes:list[dict[str,Moves]]= []
    for _ in range(numberOfCases):
        c = Cube3x3()
        scram = c.apply_randomScramble(scrambleLimit)
        solver = solver_class(c, w, True) #type: ignore
        moves = func(solver) #type: ignore
        if not check_func(solver): #type: ignore
            fails.append(dict(scramble=scram, solution=moves))
            if breakAtFirstFail:
                break
        elif len(passes) < getpasses:
            passes.append(dict(scramble=scram, solution=moves))
    return dict(fails=fails, passes=passes)

def testFirstCross(*,numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False, getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    return test(FirstCross, FirstCross.solve_first_cross, FirstCross.check_first_cross,
                numberOfCases, scrambleLimit, breakAtFirstFail, getpasses)

def testFirstCorners(*,numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False, getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    return test(FirstCorners, FirstCorners.solve_first_corners, FirstCorners.check_first_corners,
                numberOfCases, scrambleLimit, breakAtFirstFail, getpasses)

def testFirstLayer(*,numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False, getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    return test(FirstLayer, FirstLayer.solve_first_layer, FirstLayer.check_first_layer,
                numberOfCases, scrambleLimit, breakAtFirstFail, getpasses)

def testTillSecondLayer(*,numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False, getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    return test(FirstSecondLayer, FirstSecondLayer.solve_till_second_layer, FirstSecondLayer.check_second_layer,
                numberOfCases, scrambleLimit, breakAtFirstFail, getpasses)

def testOLL(
        numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False,
        getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    fails:list[dict[str,Moves]] = []
    passes:list[dict[str,Moves]]= []
    for _ in range(numberOfCases):
        c = Cube3x3()
        oll_edge = random.choice(list(Algo.OLL.Edges))
        oll_corner = random.choice(list(Algo.OLL.Corners))
        solver = LastLayer(c, w, True) #type: ignore
        scram = solver.apply_algo(random.choice(solver.side_faceids), oll_edge) + solver.apply_algo(random.choice(solver.side_faceids), oll_corner)
        moves = solver.solve_OLL_edges() + solver.solve_OLL_corners()
        if not solver.check_OLL(): #type: ignore
            fails.append(dict(scramble=scram, solution=moves))
            if breakAtFirstFail:
                break
        elif len(passes) < getpasses:
            passes.append(dict(scramble=scram, solution=moves))
    return dict(fails=fails, passes=passes)

def testOLLcorners(
        numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False,
        getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    fails:list[dict[str,Moves]] = []
    passes:list[dict[str,Moves]]= []
    for _ in range(numberOfCases):
        c = Cube3x3()
        solver = LastLayer(c, w, True) #type: ignore
        scram = solver.apply_algo(random.choice(solver.side_faceids), random.choice(list(Algo.OLL.Corners)))
        scram += solver.apply_algo(random.choice(solver.side_faceids), random.choice(list(Algo.OLL.Corners)))
        moves = solver.solve_OLL_corners()
        if not solver.check_OLL_corners(): #type: ignore
            fails.append(dict(scramble=scram, solution=moves))
            if breakAtFirstFail:
                break
        elif len(passes) < getpasses:
            passes.append(dict(scramble=scram, solution=moves))
    return dict(fails=fails, passes=passes)


