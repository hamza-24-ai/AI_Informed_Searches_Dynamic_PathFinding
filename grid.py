import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button, TextBox
import random

# Cell types
EMPTY    = 0
WALL     = 1
START    = 2
GOAL     = 3
VISITED  = 4
FRONTIER = 5
PATH     = 6

COLORS = {
    EMPTY:    [1.0, 1.0, 1.0],
    WALL:     [0.2, 0.2, 0.2],
    START:    [0.0, 0.8, 0.0],
    GOAL:     [1.0, 0.2, 0.2],
    VISITED:  [0.4, 0.6, 1.0],
    FRONTIER: [1.0, 1.0, 0.0],
    PATH:     [0.0, 0.9, 0.4],
}


class Grid:
    def __init__(self, rows=20, cols=20):
        self.rows  = rows
        self.cols  = cols
        self.start = (0, 0)
        self.goal  = (rows - 1, cols - 1)
        self.grid  = np.zeros((rows, cols), dtype=int)
        self.grid[self.start] = START
        self.grid[self.goal]  = GOAL
        self.fig = None
        self.ax  = None
        self.img = None

    def resize(self, rows, cols):
        self.rows  = rows
        self.cols  = cols
        self.start = (0, 0)
        self.goal  = (rows - 1, cols - 1)
        self.grid  = np.zeros((rows, cols), dtype=int)
        self.grid[self.start] = START
        self.grid[self.goal]  = GOAL

    def generate_random_maze(self, density=0.3):
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) != self.start and (r, c) != self.goal:
                    if random.random() < density:
                        self.grid[r][c] = WALL
        self.grid[self.start] = START
        self.grid[self.goal]  = GOAL

    def reset_search(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] in (VISITED, FRONTIER, PATH):
                    self.grid[r][c] = EMPTY
        self.grid[self.start] = START
        self.grid[self.goal]  = GOAL

    def set_cell(self, r, c, cell_type):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = cell_type

    def is_walkable(self, r, c):
        return (0 <= r < self.rows and
                0 <= c < self.cols and
                self.grid[r][c] != WALL)

    def get_neighbors(self, r, c):
        result = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if self.is_walkable(nr, nc):
                result.append((nr, nc))
        return result

    def to_color_array(self):
        img = np.zeros((self.rows, self.cols, 3))
        for r in range(self.rows):
            for c in range(self.cols):
                img[r][c] = COLORS[self.grid[r][c]]
        return img

    def redraw(self):
        self.img.set_data(self.to_color_array())
        self.img.set_extent([-0.5, self.cols - 0.5, self.rows - 0.5, -0.5])
        self.ax.set_xlim(-0.5, self.cols - 0.5)
        self.ax.set_ylim(self.rows - 0.5, -0.5)
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()


def setup_display(grid):
    plt.ion()
    fig, ax = plt.subplots(figsize=(13, 7))
    # Plot occupies left 60%, right 38% is control panel
    plt.subplots_adjust(left=0.03, right=0.60, top=0.95, bottom=0.05)

    grid.fig = fig
    grid.ax  = ax

    img = ax.imshow(
        grid.to_color_array(),
        interpolation='nearest',
        extent=[-0.5, grid.cols - 0.5, grid.rows - 0.5, -0.5],
        aspect='auto'
    )
    grid.img = img

    ax.set_xticks(np.arange(-0.5, grid.cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.rows, 1), minor=True)
    ax.grid(which='minor', color='gray', linewidth=0.3)
    ax.tick_params(which='both', bottom=False, left=False,
                   labelbottom=False, labelleft=False)
    ax.set_title("Dynamic Pathfinding Agent", fontsize=13)
    ax.set_xlim(-0.5, grid.cols - 0.5)
    ax.set_ylim(grid.rows - 0.5, -0.5)

    return fig, ax, img


def add_controls(grid, callbacks):
    fig = grid.fig
    c   = '0.85'

    # ── Right panel layout ──────────────────────────────────────────
    # Panel starts at x=0.62, width=0.36 (ends at 0.98)
    # Each button: [x, y_bottom, width, height]
    # Top section: action buttons
    ax_run = fig.add_axes([0.62, 0.88, 0.36, 0.06])
    ax_rst = fig.add_axes([0.62, 0.81, 0.36, 0.06])
    ax_gen = fig.add_axes([0.62, 0.74, 0.36, 0.06])

    # Middle section: toggle buttons
    ax_alg = fig.add_axes([0.62, 0.63, 0.36, 0.06])
    ax_heu = fig.add_axes([0.62, 0.56, 0.36, 0.06])
    ax_dyn = fig.add_axes([0.62, 0.49, 0.36, 0.06])

    # Grid size section: compact textboxes (short width) + Apply button
    # Rows label+box
    ax_row = fig.add_axes([0.76, 0.40, 0.22, 0.05])
    ax_col = fig.add_axes([0.76, 0.34, 0.22, 0.05])
    ax_den = fig.add_axes([0.76, 0.28, 0.22, 0.05])
    ax_apl = fig.add_axes([0.62, 0.21, 0.36, 0.05])

    btn_run = Button(ax_run, 'Run',             color=c)
    btn_rst = Button(ax_rst, 'Reset',           color=c)
    btn_gen = Button(ax_gen, 'Generate Maze',   color=c)
    btn_alg = Button(ax_alg, 'Algo: A*',        color=c)
    btn_heu = Button(ax_heu, 'Heur: Manhattan', color=c)
    btn_dyn = Button(ax_dyn, 'Dynamic: OFF',    color=c)
    txt_row = TextBox(ax_row, 'Rows: ',    initial=str(grid.rows))
    txt_col = TextBox(ax_col, 'Cols: ',    initial=str(grid.cols))
    txt_den = TextBox(ax_den, 'Density: ', initial='0.3')
    btn_apl = Button(ax_apl, 'Apply Size', color=c)

    btn_run.on_clicked(callbacks['run'])
    btn_rst.on_clicked(callbacks['reset'])
    btn_gen.on_clicked(callbacks['generate'])
    btn_alg.on_clicked(callbacks['toggle_algo'])
    btn_heu.on_clicked(callbacks['toggle_heuristic'])
    btn_dyn.on_clicked(callbacks['toggle_dynamic'])
    btn_apl.on_clicked(callbacks['apply_size'])

    # ALL stored — prevents garbage collection
    return {
        'btn_run': btn_run, 'btn_rst': btn_rst, 'btn_gen': btn_gen,
        'btn_alg': btn_alg, 'btn_heu': btn_heu, 'btn_dyn': btn_dyn,
        'btn_apl': btn_apl,
        'txt_row': txt_row, 'txt_col': txt_col, 'txt_den': txt_den,
    }


def add_legend(grid):
    """
    Bottom-right of right panel: color legend (2 columns).
    x=0.80, y=0.01, width=0.18, height=0.17
    """
    items = [
        (COLORS[START],    'Start'),
        (COLORS[GOAL],     'Goal'),
        (COLORS[WALL],     'Wall'),
        (COLORS[FRONTIER], 'Frontier'),
        (COLORS[VISITED],  'Visited'),
        (COLORS[PATH],     'Path'),
    ]
    ax_leg = grid.fig.add_axes([0.80, 0.01, 0.18, 0.17])
    ax_leg.axis('off')
    patches = [mpatches.Patch(color=col, label=lbl) for col, lbl in items]
    ax_leg.legend(
        handles=patches, loc='center', fontsize=8,
        ncol=2, framealpha=0.9, facecolor='#f0f0f0',
        edgecolor='gray', title='Legend', title_fontsize=8
    )


def connect_mouse(grid):
    pressing = [False]

    def on_press(event):
        if event.inaxes != grid.ax:
            return
        pressing[0] = True
        handle(event)

    def on_release(event):
        pressing[0] = False

    def on_motion(event):
        if pressing[0] and event.inaxes == grid.ax:
            handle(event)

    def handle(event):
        c = int(round(event.xdata))
        r = int(round(event.ydata))
        if not (0 <= r < grid.rows and 0 <= c < grid.cols):
            return
        if (r, c) == grid.start or (r, c) == grid.goal:
            return
        if event.button == 1:
            grid.set_cell(r, c, WALL)
        elif event.button == 3:
            grid.set_cell(r, c, EMPTY)
        grid.redraw()

    grid.fig.canvas.mpl_connect('button_press_event',   on_press)
    grid.fig.canvas.mpl_connect('button_release_event', on_release)
    grid.fig.canvas.mpl_connect('motion_notify_event',  on_motion)