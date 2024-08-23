from noq_solver import parse
from constants import *
import copy
from profiler import *

def get_neighbors(cell):
    dirs = ["up", "left", "down", "right"]
    neighbors = [ add(cell, DIRECTIONS[direction]) for direction in dirs]

    def valid(square):
        return square[0] >= 0 and square[0] < PUZZLE_SIZE[0] and square[1] >= 0 and square[1] < PUZZLE_SIZE[1]

    legal = []
    for neighbor in neighbors:
        if valid(neighbor):
            legal.append(neighbor)
    
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

            neighbors = get_neighbors([r,c])
            count = 0
            for nr, nc in neighbors:
                neighbor = grid[nr][nc]
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
    
    return "\n".join(printed_rows) + COLORS["ENDC"]
    
def find_paths(solution_grid, sources):
    print("Solved: ")
    print(colored_board(solution_grid, sources))

    source_set = copy.deepcopy(sources)

    paths = []
    for r in range(len(solution_grid)):
        for c in range(len(solution_grid[0])):
            cell = solution_grid[r][c]
            if len(cell) == 2:
                source = cell[1:]
                if not source in source_set: # this is the end of a path
                    continue
                
                path = []
                stack = [[r,c]] # iterative dfs to get pathpoints
                while len(stack) > 0:

                    popped = stack.pop()
                    path.append(popped)
                    neighbors = get_neighbors(popped)
                    # print(stack, path, neighbors)

                    for neighbor_coord in neighbors:
                        neighbor = solution_grid[neighbor_coord[0]][neighbor_coord[1]]
                        neighbor = neighbor[1:] if len(neighbor) == 2 else neighbor
                        # print(neighbor_coord, neighbor, neighbor == source and not neighbor_coord in path)

                        if neighbor == source and not neighbor_coord in path:
                            stack.append(neighbor_coord)
                
                paths.append(path)
                # print(f"appended {paths}")
                source_set.remove(source)
    return paths

puzzle_str ="""
1.2.3
..4.5
.....
.2.3.
.145.
"""    

if __name__ == "__main__":
    sources, grid = parse(puzzle_str)
    start_profiler()
    solution = solve(grid, sources)

    if solution:
        paths = find_paths(solution, sources)
        print(paths)
    else:
        print("No solution found.")
    
    end_profiler()