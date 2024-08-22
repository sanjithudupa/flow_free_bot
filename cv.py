import pyautogui
from constants import *
import time
import math

def isBlack(color):
    return color[0] < 50 and color[1] < 50 and color[2] < 50

def colorDistance(color1, color2):
    return math.sqrt((color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + (color1[2] - color2[2])**2)

alphabet = "abcdefghijklmnopqrstuvwxyz".split()

def to_hex(key):
    if key <= 9:
        return key
    diff = key - 10
    return alphabet[diff]


def get_puzzle_str():

    image = pyautogui.screenshot(region=(TOP_LEFT[0], TOP_LEFT[1], SIZE[0], SIZE[1]))

    grid = ""
    colors = {}

    for row in range(PUZZLE_SIZE[0]):
        for col in range(PUZZLE_SIZE[1]):
            color = image.getpixel(getImageLocation([row, col]))
            if isBlack(color):
                grid += "."
                continue
            
            found = False
            for checkAgainst in colors:
                if colorDistance(color, checkAgainst) < 10:
                    found = True
                    grid += str(colors[checkAgainst])
            
            if not found:
                colors[color] = len(colors) + 1
                grid += str(len(colors))
        grid += "\n"
    return grid