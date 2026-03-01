import time
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from grid import Grid, setup_display, add_controls, connect_mouse, WALL, PATH, EMPTY
from algorithm import gbfs, astar, manhattan, euclidean, mark_path

# ─── App State

grid = Grid(20, 20)

state = {
    'algo':      'gbfs',       # 'astar' or 'gbfs'
    'heuristic': 'manhattan',   # 'manhattan' or 'euclidean'
    'dynamic':   False,         # dynamic obstacle mode
    'running':   False,
}

metrics = {
    'nodes':  0,
    'cost':   0,
    'time_ms': 0,
}

metrics_text = None  # will hold the matplotlib text object