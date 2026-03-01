import heapq
import math
from grid import EMPTY, WALL, START, GOAL, VISITED, FRONTIER, PATH


# ─── Heuristics ───────────────────────────────────────────────────────────────

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)