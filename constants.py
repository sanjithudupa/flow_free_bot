def add(coord1, coord2):
    return [coord1[0] + coord2[0], coord1[1] + coord2[1]]

def divideVec(coord1, coord2):
    return [coord1[0] / coord2[0], coord1[1] / coord2[1]]

def divideScalar(coord1, scalar):
    return divideVec(coord1, [scalar, scalar])

TOP_LEFT = [0, 193]
SIZE = [715, 715]
BOTTOM_RIGHT = add(TOP_LEFT, SIZE)

rows = 8
cols = 8
PUZZLE_SIZE = [rows, cols]
SQUARE_SIZE = divideVec(SIZE, PUZZLE_SIZE)

OFFSET = divideScalar(SQUARE_SIZE, 2)

SCALE_FACTOR = 2338/1168

SQUARES = [[
    add(add(TOP_LEFT, [SQUARE_SIZE[0] * col, SQUARE_SIZE[0] * row]), OFFSET) for col in range(PUZZLE_SIZE[1])
] for row in range(PUZZLE_SIZE[0])]

CLICK_POS_30S = [250, 270] # [250, 563] # [250, 270]

def asTuple(coord):
    return (coord[0], coord[1])

IMAGE_SQUARES = [[
    asTuple(add([SQUARE_SIZE[0] * col, SQUARE_SIZE[0] * row], OFFSET)) for col in range(PUZZLE_SIZE[1])
] for row in range(PUZZLE_SIZE[0])]

def getLocation(gridCell):
    return SQUARES[gridCell[0]][gridCell[1]]

def getImageLocation(gridCell):
    return IMAGE_SQUARES[gridCell[0]][gridCell[1]]

def asScreen(coord):
    return asTuple(divideScalar(coord, SCALE_FACTOR))