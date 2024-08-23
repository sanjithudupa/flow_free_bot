from solver import parse
from constants import *
import copy

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
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == ".":
                for source in sources:
                    np = copy.deepcopy(grid)
                    np[r][c] = source
                    if isValidGrid(np):
                        result = dfs(np, sources)
                        if result is not None:
                            return result
                return None  # If no valid path, return None
    return grid

def try_solution(grid, sources):
    solvable = isValidGrid(grid)
    if not solvable:
        return None

    solved = dfs(grid, sources)
    return solved

def has_empty(grid):
    for row in grid:
        for cell in row:
            if cell == ".":
                return True
    return False

def solve(grid, sources):
    max_attempts = 1000  # Define a maximum number of attempts to avoid infinite loops
    count = 0
    
    while count < max_attempts:
        solution = try_solution(copy.deepcopy(grid), sources)
        
        if solution is not None and not has_empty(solution) and isValidGrid(solution):
            return solution
        
        count += 1
        print(f"Try again {count}")

    print("Unable to find a solution within the maximum attempts.")
    return None
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
    

if __name__ == "__main__":
    puzzle_str ="""
1.2.3
..4.5
.....
.2.3.
.145.
"""
    sources, grid = parse(puzzle_str)
    solution = solve(grid, sources)

    if solution:
        print(colored_board(solution, sources))
    else:
        print("No solution found.")