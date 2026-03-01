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

def setup_display(grid):
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(left=0.05, right=0.75, top=0.95, bottom=0.05)

    grid.fig = fig
    grid.ax = ax

    color_array = grid.to_color_array()
    img = ax.imshow(color_array, interpolation='nearest')
    grid.img = img

    # Draw grid lines
    ax.set_xticks(np.arange(-0.5, grid.cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.rows, 1), minor=True)
    ax.grid(which='minor', color='gray', linewidth=0.3)
    ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.set_title("Dynamic Pathfinding Agent", fontsize=13)

    # Legend
    legend_patches = [
        mpatches.Patch(color=COLORS[START], label='Start'),
        mpatches.Patch(color=COLORS[GOAL], label='Goal'),
        mpatches.Patch(color=COLORS[WALL], label='Wall'),
        mpatches.Patch(color=COLORS[FRONTIER], label='Frontier'),
        mpatches.Patch(color=COLORS[VISITED], label='Visited'),
        mpatches.Patch(color=COLORS[PATH], label='Path'),
    ]
    ax.legend(handles=legend_patches, loc='upper left',
              bbox_to_anchor=(1.02, 1), fontsize=9, framealpha=0.9)

    return fig, ax, img

def add_controls(grid, callbacks):
    """
    callbacks is a dict with keys:
    'run', 'reset', 'generate', 'toggle_algo', 'toggle_heuristic', 'toggle_dynamic'
    """
    fig = grid.fig

    btn_color = '0.85'

    # Button positions [left, bottom, width, height]
    ax_run     = fig.add_axes([0.77, 0.82, 0.20, 0.05])
    ax_reset   = fig.add_axes([0.77, 0.75, 0.20, 0.05])
    ax_gen     = fig.add_axes([0.77, 0.68, 0.20, 0.05])
    ax_algo    = fig.add_axes([0.77, 0.58, 0.20, 0.05])
    ax_heur    = fig.add_axes([0.77, 0.51, 0.20, 0.05])
    ax_dyn     = fig.add_axes([0.77, 0.44, 0.20, 0.05])
    ax_rows    = fig.add_axes([0.77, 0.34, 0.20, 0.05])
    ax_cols    = fig.add_axes([0.77, 0.27, 0.20, 0.05])
    ax_density = fig.add_axes([0.77, 0.20, 0.20, 0.05])
    ax_apply   = fig.add_axes([0.77, 0.13, 0.20, 0.05])

    btn_run     = Button(ax_run,     'Run',          color=btn_color)
    btn_reset   = Button(ax_reset,   'Reset',        color=btn_color)
    btn_gen     = Button(ax_gen,     'Generate Maze',color=btn_color)
    btn_algo    = Button(ax_algo,    'Algo: A*',     color=btn_color)
    btn_heur    = Button(ax_heur,    'Heur: Manhattan', color=btn_color)
    btn_dyn     = Button(ax_dyn,     'Dynamic: OFF', color=btn_color)

    txt_rows    = TextBox(ax_rows,    'Rows: ',    initial=str(grid.rows))
    txt_cols    = TextBox(ax_cols,    'Cols: ',    initial=str(grid.cols))
    txt_density = TextBox(ax_density, 'Density: ', initial='0.3')
    btn_apply   = Button(ax_apply,   'Apply Size', color=btn_color)

    btn_run.on_clicked(callbacks['run'])
    btn_reset.on_clicked(callbacks['reset'])
    btn_gen.on_clicked(callbacks['generate'])
    btn_algo.on_clicked(callbacks['toggle_algo'])
    btn_heur.on_clicked(callbacks['toggle_heuristic'])
    btn_dyn.on_clicked(callbacks['toggle_dynamic'])
    btn_apply.on_clicked(callbacks['apply_size'])

    controls = {
        'btn_algo': btn_algo,
        'btn_heur': btn_heur,
        'btn_dyn':  btn_dyn,
        'txt_rows': txt_rows,
        'txt_cols': txt_cols,
        'txt_density': txt_density,
    }

    return controls
