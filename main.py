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

# ─── Helpers

def get_heuristic():
    if state['heuristic'] == 'manhattan':
        return manhattan
    return euclidean

def update_metrics_display():
    if metrics_text:
        metrics_text.set_text(
            f"Nodes Visited : {metrics['nodes']}\n"
            f"Path Cost     : {metrics['cost']}\n"
            f"Time (ms)     : {metrics['time_ms']:.1f}"
        )
        grid.fig.canvas.draw_idle()

# ─── Animation draw callback ──────────────────────────────────────────────────

def animated_draw():
    grid.draw()
    plt.pause(0.03)

# ─── Dynamic obstacle spawning ────────────────────────────────────────────────

def spawn_obstacle_on_path(current_path, current_pos_idx):
    """Randomly spawn a wall on the remaining path (ahead of agent)."""
    ahead = current_path[current_pos_idx + 1:]  # don't block already-visited
    candidates = [n for n in ahead if n != grid.goal]
    if candidates and random.random() < 0.25:   # 25% chance each step
        chosen = random.choice(candidates)
        grid.set_cell(chosen[0], chosen[1], WALL)
        return chosen
    return None

# ─── Main Run Logic ───────────────────────────────────────────────────────────

def run_search(event=None):
    if state['running']:
        return
    state['running'] = True

    grid.reset_search()
    grid.draw()
    plt.pause(0.05)

    heuristic_fn = get_heuristic()
    start_time   = time.time()

    # Run chosen algorithm
    if state['algo'] == 'astar':
        path, nodes, cost = astar(grid, heuristic_fn, draw_callback=animated_draw)
    else:
        path, nodes, cost = gbfs(grid, heuristic_fn, draw_callback=animated_draw)

    elapsed = (time.time() - start_time) * 1000

    if path is None:
        print("No path found!")
        metrics['nodes']   = nodes
        metrics['cost']    = 0
        metrics['time_ms'] = elapsed
        update_metrics_display()
        state['running'] = False
        return

