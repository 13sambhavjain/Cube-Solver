from core import Cube3x3, w, Moves, g
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
        solver = solver_class(c, g, True) #type: ignore
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
    return test(Solver3x3, Solver3x3.solve_till_second_layer, Solver3x3.check_second_layer,
                numberOfCases, scrambleLimit, breakAtFirstFail, getpasses)

def testOLL(
        numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False,
        getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    fails:list[dict[str,Moves]] = []
    passes:list[dict[str,Moves]]= []
    for _ in range(numberOfCases):
        if _%1000 == 0:
            print(_)
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

def test_solve_cube(*,numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False, getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    return test(Solver3x3, Solver3x3.solve_cube, FirstCorners.check_solved,
                numberOfCases, scrambleLimit, breakAtFirstFail, getpasses)

def test_oll_pll(
        numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False,
        getpasses: int = 10) -> dict[str,list[dict[str,Moves]]]:
    fails:list[dict[str,Moves]] = []
    passes:list[dict[str,Moves]]= []
    for _ in range(numberOfCases):
        c = Cube3x3()
        oll_edge = random.choice(list(Algo.OLL.Edges))
        oll_corner = random.choice(list(Algo.OLL.Corners))
        # pll_corner = random.choice(list(Algo.PLL.Corners))
        # pll_edge = random.choice(list(Algo.PLL.Edges))
        solver = Solver3x3(c, w, True) #type: ignore
        scram = solver.apply_algo(random.choice(solver.side_faceids), oll_edge) + solver.apply_algo(random.choice(solver.side_faceids), oll_corner)
        moves = solver.solve_OLL_edges() + solver.solve_OLL_corners() + solver.solve_PLL()
        if not solver.check_solved(): #type: ignore
            fails.append(dict(scramble=scram, solution=moves))
            if breakAtFirstFail:
                break
        elif len(passes) < getpasses:
            passes.append(dict(scramble=scram, solution=moves))
    return dict(fails=fails, passes=passes)


