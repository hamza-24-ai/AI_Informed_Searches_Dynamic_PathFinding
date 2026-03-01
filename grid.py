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

class Grid:
    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)

        # Default start and goal
        self.start = (0, 0)
        self.goal = (rows - 1, cols - 1)

        self.grid[self.start] = START
        self.grid[self.goal] = GOAL

        # For drawing
        self.fig = None
        self.ax = None
        self.img = None

        # Mode: 'wall' or 'start' or 'goal'
        self.edit_mode = 'wall'

    def resize(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.start = (0, 0)
        self.goal = (rows - 1, cols - 1)
        self.grid[self.start] = START
        self.grid[self.goal] = GOAL

    def generate_random_maze(self, density=0.3):
        # Reset grid
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) != self.start and (r, c) != self.goal:
                    if random.random() < density:
                        self.grid[r][c] = WALL
        self.grid[self.start] = START
        self.grid[self.goal] = GOAL

    def reset_search(self):
        # Clear only visited, frontier, path cells
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] in (VISITED, FRONTIER, PATH):
                    self.grid[r][c] = EMPTY
        self.grid[self.start] = START
        self.grid[self.goal] = GOAL

    def set_cell(self, r, c, cell_type):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = cell_type

    def get_cell(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return None

    def is_walkable(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != WALL

    def get_neighbors(self, r, c):
        # 4-directional movement
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.is_walkable(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

    def to_color_array(self):
        color_grid = np.zeros((self.rows, self.cols, 3))
        for r in range(self.rows):
            for c in range(self.cols):
                color_grid[r][c] = COLORS[self.grid[r][c]]
        return color_grid

    def draw(self):
        self.img.set_data(self.to_color_array())
        self.fig.canvas.draw_idle()