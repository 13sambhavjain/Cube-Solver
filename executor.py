from core import *
from tests.test_solver3x3 import testFirstCross, testFirstCorners
from utils.prints2structure import print2Cube3x3
def main():
    result = testFirstCorners(numberOfCases=10000, breakAtFirstFail=True)
    if result['fails']:
        print("Failed")
        return
    else:
        k = result["passes"]
        for scam in k:
            c = Cube3x3()
            c.apply_moves(scam["scram"])
            print(f"{scam["scram"]}")
            print(c)
            c.apply_moves(scam["moves"])
            print(f"{scam["moves"]}, {scam['moves'].comment=}")
            print(c)
            print("\n\n\n")
#         print2Cube3x3("""G O O 
# G W W
# W W Y

# Y B B   G O Y
# Y B B   O O Y
# W W O   B G G

#         R R R   R G G
#         R Y Y   R G G
#         W B B   O O Y

#                 R Y W
#                 R R W
#                 O B B""")












if __name__ == "__main__":
    main()