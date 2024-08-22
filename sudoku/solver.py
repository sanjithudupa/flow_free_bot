## super simple backtracking-based sudoku solver I wrote to get an idea for how flow backtracking could work

puzzle_str = """
.7.583.2.
.592..3..
34...65.7
795...632
..36971..
68...27..
914835.76
.3.7.1495
567429.13
"""

def parse(puzzle_str):
    lines = puzzle_str.split("\n")
    grid = []
    for line in lines:
        if len(line) == 0:
            continue
    
        grid.append(list(line))
    return grid

# horrendous but copy pasted from my leetcode solution to this problem so i didnt have to write it again
# realistically there is no need to search all over the grid again each time but its only 81 squares so np
def isValidSudoku(board):
    col_sets = [set() for _ in range(9)]
    subbox_sets = [[set()for _ in range(3)] for _ in range(3)] #for simplicty, making it a 2d array

    for row_index in range(0, 9):
        row_set = set()
        for col_index in range(0, 9):
            cell = board[row_index][col_index]

            if cell == ".":
                continue
            
            # check if cell has appeared in this row
            if cell in row_set:
                # print(f"row: cell {cell} at board[{row_index}][{col_index}]")
                return False
            row_set.add(cell)

            # check if cell has appeared in this column
            if cell in col_sets[col_index]:
                # print(f"col: cell {cell} at board[{row_index}][{col_index}]")
                return False
            col_sets[col_index].add(cell)

            # check if cell has appeared in this subbox
            row_sub = row_index // 3
            col_sub = col_index // 3
            if cell in subbox_sets[row_sub][col_sub]:
                # print(f"subbox: cell {cell} at board[{row_index}][{col_index}], sub[{row_sub}][{col_sub}]")
                return False
            subbox_sets[row_sub][col_sub].add(cell)

    return True

def get_unsolved_squares(puzzle):
    squares = []
    i = 0
    for row in puzzle:
        j = 0
        for square in row:
            if square == ".":
                squares.append([i, j])
            j += 1
        i += 1
    return squares

def dfs(puzzle):
    sawOne = False

    r = 0
    for row in puzzle:
        c = 0
        for square in row:
            if square == ".":
                sawOne = True
                for i in range(1, 10):
                    np = puzzle.copy()
                    np[r][c] = i
                    if isValidSudoku(np):
                        return dfs(np)
            c += 1
        r += 1

    if not sawOne:
        return puzzle
    
    return puzzle

def solve(puzzle):
    solvable = isValidSudoku(puzzle)
    if not solvable:
        raise ValueError("NOT SOLVABLE")

    solved = dfs(puzzle)
    return solved

puzzle = parse(puzzle_str)
solution = solve(puzzle)
print(solution)