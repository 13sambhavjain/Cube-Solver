from core import *
from tests.test_solver3x3 import *

def printcases(cases):
    for case in cases:
        c = Cube3x3()
        c.apply_moves(case["scramble"])
        print(f"{case["scramble"]}, {case['scramble'].comment}")
        print(c)
        # if case["solution"]:
        c.apply_moves(case["solution"])
        print(f"{case["solution"]}, {case['solution'].comment=}")
        print(c)
        print("\n\n\n")

def check_print_result(result):
    if result['fails']:
        print("Fails = ")
        printcases(result["fails"])
        print("Failed")
        return
    else:
        print("Passes = ")
        printcases(result["passes"])
        print("Passed")


def main():
    result = test_solve_cube(numberOfCases=1000, breakAtFirstFail=True)
    check_print_result(result)
    # c = Cube3x3()
    # solver = LastLayer(c, w)
    # print(solver.apply_algo(FaceId.green, Algo.OLL.Edges.dot_shape))
    # print(solver.apply_algo(FaceId.red, Algo.OLL.Corners.Sune))
    # print(c)
    # print(moves:= solver.solve_OLL() + solver.solve_PLL())
    # print(moves.comment)
    # print(solver.check_solved())
    # print(c)

if __name__ == "__main__":
    main()