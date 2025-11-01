from CubeClass import *
def test_firstcross():
    failed = []
    for _ in range(100):
        c = Cube()
        scram = c.randomScramble(20)
        c.first_cross()
        if not c.solved():
            failed.append(scram)
            print(scram)
            c = input()


test_firstcross()