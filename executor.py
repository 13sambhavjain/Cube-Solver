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
        print("Failed")
        printcases(result["fails"])
        return
    else:
        printcases(result["passes"])


def main():
    result = testOLLcorners(numberOfCases=10000, breakAtFirstFail=True)
    check_print_result(result)
    

if __name__ == "__main__":
    main()