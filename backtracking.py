from solver import parse
from constants import *
import copy

puzzle_str ="""
1.2.3
..4.5
.....
.2.3.
.145.
"""

# puzzle_str = """
# ...12
# 1....
# ..3..
# ...4.
# 243..
# """

def get_neighbors(grid, cell):
    dirs = ["up", "left", "down", "right"]
    neighbors = [ add(cell, DIRECTIONS[direction]) for direction in dirs]

    def valid(square):
        return square[0] >= 0 and square[0] < PUZZLE_SIZE[0] and square[1] >= 0 and square[1] < PUZZLE_SIZE[1]

    legal = []
    for neighbor in neighbors:
        if valid(neighbor):
            legal.append(grid[neighbor[0]][neighbor[1]])
    
    return legal
    # return [grid[neighbor[0]][neighbor[1]] for neighbor in neighbors if valid(neighbor)]

def parse(puzzle_str):
    lines = puzzle_str.split("\n")
    columns = len(lines)
    grid = []
    sources = set()
    for line in lines:
        if len(line) == 0:
            continue

        row = []
        for c in line:
            row.append(c if c == "." else f"s{c}")
            sources.add(c)
        grid.append(row)

    sources.remove(".")
    return (sources, grid)

def isValidGrid(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            cell = grid[r][c]

            if cell == ".":
                continue

            is_source =  cell[:1] == "s" # it is a source node
            cell_color = cell[1:] if is_source else cell

            neighbors = get_neighbors(grid, [r,c])
            count = 0
            for neighbor in neighbors:
                neighbor_color = neighbor[1:] if neighbor[:1] == "s" else neighbor
                count += 1 if neighbor == "." or cell_color == neighbor_color else 0
                
            if count < (1 if is_source else 2):
                return False
            
    return True

def dfs(grid, sources):
    sawOne = False

    r = 0
    for row in grid:
        c = 0
        for square in row:
            if square == ".":
                sawOne = True
                for source in sources:
                    np = copy.deepcopy(grid)
                    np[r][c] = source
                    if isValidGrid(np):
                        return dfs(np, sources)
            c += 1
        r += 1

    if not sawOne:
        return grid
    return grid

def _solve(grid, sources):
    solvable = isValidGrid(grid)
    if not solvable:
        return

    solved = dfs(grid, sources)
    return solved

def format_solution(solution_grid):
    for r in len(solution_grid):
        for c in len(solution_grid[r]):
            solution_grid[r][c] = solution_grid[r][c].replace("s", "")
    
    return solution_grid

def has_empty(grid):
    for row in grid:
        for cell in row:
            if cell == ".":
                return True
    return False

def solve(grid, sources):
    count = 1
    
    while True: # deepcopy should have fixed the need for this
        solution = _solve(copy.deepcopy(grid), sources)
        
        if not has_empty(solution) and solution != None and isValidGrid(solution):
            break
        
        count += 1
        print("try again")

    # print(f"Num solutions {count}")
    return (solution)
# rules: each thing must either have an empty square or two neighboring

def colored_board(solution, sources):
    source_list = list(sources)
    color_keys = list(COLORS.keys())

    printed_rows = []
    for row in solution:
        print_row = ""
        for col in row:
            cell = col if len(col) == 1 else col[1:]
            color_index = source_list.index(cell) % len(color_keys)
            print_row += (f"{COLORS[color_keys[color_index]]}{cell}")
        printed_rows.append(print_row)
    
    return "\n".join(printed_rows)
    


sources, grid = parse(puzzle_str)
solution = solve(grid, sources)
print(solution)
print(colored_board(solution, sources))


# neighbors = get_neighbors(grid, [1,2])
# print(neighbors)
# print(sources)

# grid[0][1] = "4"

# print(isValidGrid(grid))