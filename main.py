import time
import random
import matplotlib.pyplot as plt
from grid import (Grid, setup_display, add_controls, add_legend, connect_mouse,
                  WALL, PATH, START, GOAL)
from algorithm import gbfs, astar, manhattan, euclidean, mark_path

# ─── Global state ─────────────────────────────────────────────────────────────

grid = Grid(20, 20)

state = {
    'algo':      'astar',      # 'astar' or 'gbfs'
    'heuristic': 'manhattan',  # 'manhattan' or 'euclidean'
    'dynamic':   False,
    'running':   False,
}

metrics      = {'nodes': 0, 'cost': 0, 'time_ms': 0}
metrics_text = None
controls     = {}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_heuristic():
    return manhattan if state['heuristic'] == 'manhattan' else euclidean

def refresh():
    grid.redraw()

def animated_draw():
    grid.redraw()

def update_metrics():
    if metrics_text:
        metrics_text.set_text(
            f"Nodes Visited : {metrics['nodes']}\n"
            f"Path Cost     : {metrics['cost']}\n"
            f"Time (ms)     : {metrics['time_ms']:.1f}"
        )
        grid.fig.canvas.draw_idle()
        grid.fig.canvas.flush_events()

# ─── Dynamic obstacle spawning ────────────────────────────────────────────────

def spawn_obstacle(path, idx):
    ahead = [n for n in path[idx + 1:] if n != grid.goal]
    if ahead and random.random() < 0.25:
        chosen = random.choice(ahead)
        grid.set_cell(chosen[0], chosen[1], WALL)
        return chosen
    return None

# ─── Run search ───────────────────────────────────────────────────────────────

def run_search(event=None):
    if state['running']:
        return
    state['running'] = True

    # Save original start so we can restore after dynamic mode
    original_start = grid.start

    grid.reset_search()
    refresh()

    hfn        = get_heuristic()
    start_time = time.time()

    if state['algo'] == 'astar':
        path, nodes, cost = astar(grid, hfn, draw_callback=animated_draw)
    else:
        path, nodes, cost = gbfs(grid, hfn, draw_callback=animated_draw)

    elapsed = (time.time() - start_time) * 1000

    if path is None:
        print("No path found!")
        metrics.update({'nodes': nodes, 'cost': 0, 'time_ms': elapsed})
        update_metrics()
        state['running'] = False
        return

    if state['dynamic']:
        i = 0
        while i < len(path) - 1:
            cur     = path[i]
            blocked = spawn_obstacle(path, i)

            if blocked:
                print(f"Obstacle at {blocked} — re-planning from {cur}...")
                grid.reset_search()

                # Set new start to current agent position
                grid.start = cur
                grid.grid[cur[0]][cur[1]] = START
                # Make sure goal is still marked
                grid.grid[grid.goal[0]][grid.goal[1]] = GOAL
                refresh()

                t0 = time.time()
                if state['algo'] == 'astar':
                    path, nodes, cost = astar(grid, hfn, draw_callback=animated_draw)
                else:
                    path, nodes, cost = gbfs(grid, hfn, draw_callback=animated_draw)
                elapsed += (time.time() - t0) * 1000

                if path is None:
                    print("No path after re-planning!")
                    break
                i = 0
                continue

            # Walk one step
            if cur != grid.start and cur != grid.goal:
                grid.set_cell(cur[0], cur[1], PATH)
            refresh()
            plt.pause(0.08)
            i += 1

        # Restore original start
        grid.start = original_start
        grid.grid[original_start[0]][original_start[1]] = START
        grid.grid[grid.goal[0]][grid.goal[1]] = GOAL
        refresh()

    else:
        mark_path(grid, path)
        refresh()

    metrics.update({'nodes': nodes, 'cost': cost, 'time_ms': elapsed})
    update_metrics()
    state['running'] = False

# ─── Button callbacks ─────────────────────────────────────────────────────────

def reset(event=None):
    if state['running']:
        return
    grid.reset_search()
    refresh()
    metrics.update({'nodes': 0, 'cost': 0, 'time_ms': 0})
    update_metrics()

def generate(event=None):
    if state['running']:
        return
    try:
        density = float(controls['txt_den'].text)
    except:
        density = 0.3
    grid.generate_random_maze(density)
    refresh()

def toggle_algo(event=None):
    if state['algo'] == 'astar':
        state['algo'] = 'gbfs'
        controls['btn_alg'].label.set_text('Algo: GBFS')
    else:
        state['algo'] = 'astar'
        controls['btn_alg'].label.set_text('Algo: A*')
    grid.fig.canvas.draw_idle()
    grid.fig.canvas.flush_events()

def toggle_heuristic(event=None):
    if state['heuristic'] == 'manhattan':
        state['heuristic'] = 'euclidean'
        controls['btn_heu'].label.set_text('Heur: Euclidean')
    else:
        state['heuristic'] = 'manhattan'
        controls['btn_heu'].label.set_text('Heur: Manhattan')
    grid.fig.canvas.draw_idle()
    grid.fig.canvas.flush_events()

def toggle_dynamic(event=None):
    state['dynamic'] = not state['dynamic']
    controls['btn_dyn'].label.set_text(
        'Dynamic: ON' if state['dynamic'] else 'Dynamic: OFF'
    )
    grid.fig.canvas.draw_idle()
    grid.fig.canvas.flush_events()

def apply_size(event=None):
    if state['running']:
        return
    try:
        rows = max(5, min(int(controls['txt_row'].text), 50))
        cols = max(5, min(int(controls['txt_col'].text), 50))
    except:
        rows, cols = 20, 20

    grid.resize(rows, cols)

    # Must update extent so imshow matches new grid size
    grid.img.set_data(grid.to_color_array())
    grid.img.set_extent([-0.5, cols - 0.5, rows - 0.5, -0.5])
    grid.ax.set_xlim(-0.5, cols - 0.5)
    grid.ax.set_ylim(rows - 0.5, -0.5)
    grid.ax.set_xticks(
        [x - 0.5 for x in range(cols + 1)], minor=True)
    grid.ax.set_yticks(
        [y - 0.5 for y in range(rows + 1)], minor=True)
    grid.fig.canvas.draw()
    grid.fig.canvas.flush_events()

# ─── Setup ────────────────────────────────────────────────────────────────────

setup_display(grid)

callbacks = {
    'run':              run_search,
    'reset':            reset,
    'generate':         generate,
    'toggle_algo':      toggle_algo,
    'toggle_heuristic': toggle_heuristic,
    'toggle_dynamic':   toggle_dynamic,
    'apply_size':       apply_size,
}

controls = add_controls(grid, callbacks)
connect_mouse(grid)   # no controls_ref needed anymore

add_legend(grid)

metrics_text = grid.fig.text(
    0.62, 0.01,
    "Nodes Visited : 0\nPath Cost     : 0\nTime (ms)     : 0.0",
    fontsize=9,
    verticalalignment="bottom",
    family="monospace",
    bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.9)
)

plt.ioff()
plt.show()