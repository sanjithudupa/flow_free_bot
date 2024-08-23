from solver import parse, solve
from actor import optimize_path, control_path
from cv import get_puzzle_str
import time
import pyautogui
from constants import *

# puzzle_str ="""
# 1.2.3
# ..4.5
# .....
# .2.3.
# .145.
# """

def solve_puzzle():
    start = time.time()
    puzzle_str = get_puzzle_str()

    print(puzzle_str)
    puzzle = parse(puzzle_str)
    paths = solve(puzzle)
    optimized_paths = [optimize_path(path) for path in paths ]

    for path in optimized_paths:
        control_path(path)

    end = time.time()
    print(f"total took {end - start} seconds")

def solve_time_trial():
    print("3 seconds to get set...")
    time.sleep(3)

    pyautogui.moveTo(CLICK_POS_30S[0], CLICK_POS_30S[1])

    pyautogui.click(button="left")

    time.sleep(0.5)

    print("START")

    # global_start = time.time()
    
    while True:
        solve_puzzle()
        time.sleep(0.75)

# time.sleep(2)
# solve_puzzle()

time.sleep(2)
print(get_puzzle_str())