import pyautogui
from constants import *

# print(SQUARES)

# for row in SQUARES:
#     for square in row:
#         pyautogui.moveTo(square[0], square[1])
#         time.sleep(0.25)

# def optimize_paths(paths):
#     for path in paths:
        # for i in range(1, len(path)):
            
def optimize_path(path):
    optimized = [path[0]] # start with first element

    axis = "n"
    i = 0
    f = 1
    
    while True:
        pi = path[i]

        if f >= len(path):
            optimized.append(path[f-1])
            break

        pf = path[f]

        if axis == "n": # start of a new leg
            axis = "x" if pf[0] == pi[0] else "y"

        if pf[0 if axis == "x" else 1] == pi[0 if axis == "x" else 1]:
            f += 1
        else:
            optimized.append(path[f-1])
            i = f-1
            axis = "n"
    
    return optimized
        
        # if axis == "x":
        #     f += 0
            
        #     if pf[0] != pi[0] or f

def control_path(path):
    pyautogui.moveTo(getLocation(path[0]))
    for position in path[1:]:
        pyautogui.dragTo(getLocation(position), button="left", duration=0.0)

# o = optimize_path([
#     [0,0],
#     [1,0],
#     [2,0],
#     [3,0],
#     [3,1],
#     [3,2],
#     [2,2]
# ])

# print(o)


# paths = [[[4, 3], [4, 4], [3, 4], [2, 4], [1, 4]], [[4, 2], [3, 2], [2, 2], [1, 2]], [[4, 1], [4, 0], [3, 0], [2, 0], [1, 0], [0, 0]], [[3, 3], [2, 3], [1, 3], [0, 3], [0, 4]], [[3, 1], [2, 1], [1, 1], [0, 1], [0, 2]]]

# optimized = [ optimize_path(path) for path in paths ]


# print("GOING IN 3")

# time.sleep(3)
# for path in optimized:
#     pyautogui.moveTo(getLocation(path[0]))
#     for position in path[1:]:
#         pyautogui.dragTo(getLocation(position), button="left", duration=0.0)