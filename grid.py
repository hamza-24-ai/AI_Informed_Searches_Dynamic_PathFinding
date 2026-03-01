import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button, TextBox
import random

# Cell types
EMPTY = 0
WALL = 1
START = 2
GOAL = 3
VISITED = 4
FRONTIER = 5
PATH = 6

# Colors for each cell type
COLORS = {
    EMPTY:    [1.0, 1.0, 1.0],   # White
    WALL:     [0.2, 0.2, 0.2],   # Dark gray
    START:    [0.0, 0.8, 0.0],   # Green
    GOAL:     [1.0, 0.2, 0.2],   # Red
    VISITED:  [0.4, 0.6, 1.0],   # Blue
    FRONTIER: [1.0, 1.0, 0.0],   # Yellow
    PATH:     [0.0, 0.9, 0.4],   # Bright green
}