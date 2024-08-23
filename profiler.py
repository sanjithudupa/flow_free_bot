import time
from constants import *

# def profile(func):
#     def wrapper():
#         start = time.time()
#         out = func()
#         diff = time.time() - start
#         print(f"{COLORS["UNDERLINE"]}Execution took {diff} seconds.{COLORS["ENDC"]}")
#         return out
#     return profile

start_time = 0

def start_profiler():
    global start_time
    print(f"{COLORS["UNDERLINE"]}Start of profiler...{COLORS["ENDC"]}")
    start_time = time.time()

def end_profiler():
    print(f"{COLORS["UNDERLINE"]}Excecution took {time.time() - start_time} seconds.{COLORS["ENDC"]}")