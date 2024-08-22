from solver import parse

puzzle_str ="""
1.2.3
..4.5
.....
.2.3.
.145.
"""

def parse(puzzle_str):
    lines = puzzle_str.split("\n")
    columns = len(lines)
    grid = []
    for line in lines:
        if len(line) == 0:
            continue
        grid.append(list(line))
    return grid

print(parse(puzzle_str))