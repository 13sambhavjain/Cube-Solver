from core import *
from tests.test_solver3x3 import *

def check_print_result(result):
    if result['fails']:
        print("Failed")
        return
    else:
        passes = result["passes"]
        for case in passes:
            c = Cube3x3()
            c.apply_moves(case["scramble"])
            print(f"{case["scramble"]}")
            print(c)
            if case["solution"]:
                c.apply_moves(case["solution"])
                print(f"{case["solution"]}, {case['solution'].comment=}")
                print(c)
                print("\n\n\n")
            else:
                print("Its actually not there")

def main():
    result = testTillSecondLayer(numberOfCases=10000, breakAtFirstFail=True)
    check_print_result(result)
    

if __name__ == "__main__":
    main()