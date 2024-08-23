import json
from urllib.parse import quote
from urllib.request import urlopen
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from constants import *
from profiler import start_profiler, end_profiler

puzzle_str ="""
1.2.3
..4.5
.....
.2.3.
.145.
"""

def parse(p_str):
    lines = list(filter(None, p_str.split('\n')))

    columns = len(lines[0])
    
    filled_squares = {}
    row = 0
    for line in lines:
        if len(line) != columns:
            raise ValueError("puzzle is not rectangular")
        col = 0
        for c in line:
            if c != ".":
                num = int(c, 16) # supports up to 16 flows expressed in hexadecimal
                loc = [row*2 + 1, col*2 + 1] # convert to solver coordinate system
                filled_squares[f"{loc[0]},{loc[1]}"] = num
            col += 1
        row += 1
    
    puzzle = {
        "r": len(lines),
        "c": columns,
        "hints": filled_squares
    }
    return puzzle

def request_solution(puzzle):
    request_params = {
        "param_values": {
            "r": puzzle["r"],
            "c": puzzle["c"],
            "Use all cells": True
        },
        "grid": puzzle["hints"],
        "puzzle_type":"numberlink",
        "properties": {
            "outside":"0000",
            "border":False
        }
    }

    query = quote(json.dumps(request_params))
    url = f"http://www.noq.solutions/solver?puzzle_type=numberlink&puzzle={query}"
    
    return json.load(urlopen(url))

CONNECTIONS = { 
    "top_end": ["down"], 
    "bottom_end": ["up"], 
    "right_end": ["left"],
    "left_end": ["right"], 
    "-": ["left", "right"], 
    "1": ["up", "down"], 
    "r": ["down", "right"], 
    "7": ["down", "left"], 
    "J": ["up", "left"],
    "L": ["up", "right"] 
}

def encode(array):
    # return array[0] + (array[1] / (10 ** (array[1] // 10)))
    return f"{array[0]},{array[1]}"

def decode(string):
    # s = str(num)
    # return [int(s[:-s[::-1].find(".") - 1]), int(s[s.find(".") + 1:])]
    s_arr = string.split(",")
    return [int(s_arr[0]), int(s_arr[1])]

def parse_solution(puzzle, solution):
    w = puzzle["c"]
    h = puzzle["r"]

    grid = [[[] for x in range(w)] for y in range(h)]

    ends = [] # use as stack, used set before for faster removal, but this is better for approach

    for loc_str in solution:
        loc = loc_str.split(",")

        row = (int(loc[0]) - 1)//2
        col = (int(loc[1]) - 1)//2

        connection_type = solution[loc_str].replace(".png", "")
        edges = CONNECTIONS[connection_type]

        if "end" in connection_type:
            ends.append([row,col])

        grid[row][col] = edges

    return grid, ends

def find_paths(grid, ends):
    # rows = puzzle["r"]
    # cols = puzzle["c"]

    print(grid)
    print(ends)

    paths = []
    while len(ends) > 0: # iterate through all the ends
        current = ends.pop()
        row = current[0]
        col = current[1]
        
        last_direction = grid[row][col][0]

        print(f"Starting path {len(paths)} at end {current}")

        current_path = [[row, col]]

        while True:
            move = DIRECTIONS[last_direction]
            row += move[0]
            col += move[1]

            current_path.append([row, col])
            print(f"Added point in direction {last_direction} - {[row, col]}")

            if [row, col] in ends:
                print(f"It was an end")
                break

            next_direction = ""
            next_direction_options = grid[row][col]
            for direction in next_direction_options:
                print(f"Checking direction option {[row, col]} - {direction}")
                if direction != INVERSES[last_direction]:
                    print(f"Chosen {direction}")
                    next_direction = direction
                    break
            
            if next_direction == "":
                raise RuntimeError("Next Direction Not Allowed")
        
            last_direction = next_direction
        
        print(f"Created path {current_path}")

        paths.append(current_path)
        ends.remove(current_path[-1])
    
    return paths


def solve(puzzle):
    res = request_solution(puzzle)
    if not "num_solutions" in res:
        raise RuntimeError("No solution found")

    solution = res['1']
    grid, ends = parse_solution(puzzle, solution)
    
    paths = find_paths(grid, ends)
    return paths

paths = [[[4, 3], [4, 4], [3, 4], [2, 4], [1, 4]], [[4, 2], [3, 2], [2, 2], [1, 2]], [[4, 1], [4, 0], [3, 0], [2, 0], [1, 0], [0, 0]], [[3, 3], [2, 3], [1, 3], [0, 3], [0, 4]], [[3, 1], [2, 1], [1, 1], [0, 1], [0, 2]]]

def test_solver():
    puzzle = parse(puzzle_str)
    paths = solve(puzzle)
    print("Paths", paths)

if __name__ == "__main__":
    start_profiler()
    test_solver()
    end_profiler()

# solve(puzzle)

# print(quote('https://www.noq.solutions/solver?puzzle_type=numberlink&puzzle={"param_values":{"r":"6","c":"5","Use all cells":false},"grid":{"1,1":"1","3,1":"2","5,1":"3","7,1":"4","9,1":"5","11,1":"6"},"puzzle_type":"numberlink","properties":{"outside":"0000","border":false}}'))
# 