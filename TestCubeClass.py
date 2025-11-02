from CubeSolver import *

def testFirstCross(numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False):
    fails = []
    for _ in range(numberOfCases):
        c = Cube()
        scram = c.random(scrambleLimit)
        moves = c.first_cross()
        if not c.checkFirstCross():
            fails.append(dict(scram=scram, moves=moves))
            if breakAtFirstFail:
                break
    return fails

def testFun(applyFun, checkFun, numberOfCases=1000, scrambleLimit = 10):
    fails = []
    for case in range(numberOfCases):
        c = Cube()
        scram = c.random(scrambleLimit)
        funMoves = applyFun(c)
        if not checkFun(c):
            return dict(scram=scram, moves=funMoves)
            break
    return fails

def main():
    testFails = testFirstCross()
    print(testFails)

if __name__ == "__main__":
    main()
