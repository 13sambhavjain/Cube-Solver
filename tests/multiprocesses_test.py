from multiprocessing import Pool, cpu_count
from functools import partial
import random
from core import Cube3x3, w, Moves, g
from solver3x3 import *
import random


def _run_batch(args):
    solver_class, func, check_func, scrambleLimit, random_start_face, batch_size = args
    fails = []
    passes = []
    for _ in range(batch_size):
        c = Cube3x3(start_faceId=random.choice(list(Cube3x3.faceIds)) if random_start_face else w)
        scram = c.apply_randomScramble(scrambleLimit, True)
        solver = solver_class(c, g, True)
        moves = func(solver)
        if not check_func(solver):
            fails.append(dict(scramble=scram, solution=moves))
        elif len(passes) < 10:
            passes.append(dict(scramble=scram, solution=moves))
    return fails, passes

def test(solver_class, func, check_func,
         numberOfCases=1000, scrambleLimit=10, breakAtFirstFail=False,
         getpasses=10, random_start_face=False,
         workers=None, chunksize=10000) -> dict:

    workers = workers or cpu_count()
    chunksize = min(chunksize, numberOfCases)
    
    # split into batches
    full_batches, remainder = divmod(numberOfCases, chunksize)
    batch_sizes = [chunksize] * full_batches + ([remainder] if remainder else [])
    batch_args = [
        (solver_class, func, check_func, scrambleLimit, random_start_face, size)
        for size in batch_sizes
    ]

    all_fails = []
    all_passes = []
    completed = 0

    with Pool(workers) as pool:
        for fails, passes in pool.imap_unordered(_run_batch, batch_args):
            all_fails.extend(fails)
            all_passes.extend(passes[:max(0, getpasses - len(all_passes))])
            completed += chunksize
            print(f"\r{min(completed, numberOfCases):,} / {numberOfCases:,} completed"
                  f"  |  fails: {len(all_fails)}", end='', flush=True)
            if breakAtFirstFail and all_fails:
                pool.terminate()
                break

    print()  # newline after progress
    return dict(fails=all_fails, passes=all_passes)

def test_solve_cube(*,numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False, getpasses: int = 10, random_start_face=False) -> dict[str,list[dict[str,Moves]]]:
    return test(Solver3x3, Solver3x3.solve_cube, FirstCorners.check_solved,
                numberOfCases, scrambleLimit, breakAtFirstFail, getpasses, random_start_face)
