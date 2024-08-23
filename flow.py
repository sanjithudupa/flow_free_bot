from actor import optimize_path, control_path
from cv import get_puzzle_str
import time
import pyautogui
from constants import *
import noq_solver
import backtracking

# puzzle_str ="""
# 1.2.3
# ..4.5
# .....
# .2.3.
# .145.
# """

def get_paths(puzzle_str, approach):
    if approach == "noq":
        puzzle = noq_solver.parse(puzzle_str)
        paths = noq_solver.solve(puzzle)
        return paths
    elif approach == "backtracking":
        sources, grid = backtracking.parse(puzzle_str)
        solution = backtracking.solve(grid, sources)

        if solution:
            paths = backtracking.find_paths(solution, sources)
            return paths
        else:
            print("No solution found.")

def solve_puzzle():
    start = time.time()
    puzzle_str = get_puzzle_str()

    print("Read board from screen as: ")
    print(puzzle_str)
    
    paths = get_paths(puzzle_str, "backtracking")
    
    optimized_paths = [optimize_path(path) for path in paths ]

    for path in optimized_paths:
        control_path(path)

    end = time.time()
    print(f"{COLORS["UNDERLINE"]} total took {end - start} seconds {COLORS["ENDC"]}")

def solve_time_trial():
    print("3 seconds to get set...")
    time.sleep(3)

    pyautogui.moveTo(CLICK_POS_30S[0], CLICK_POS_30S[1])

    pyautogui.click(button="left")

    time.sleep(0.35)

    print("START")

    # global_start = time.time()
    
    while True:
        solve_puzzle()
        time.sleep(0.3125)

time.sleep(2)
solve_puzzle()
# solve_time_trial()