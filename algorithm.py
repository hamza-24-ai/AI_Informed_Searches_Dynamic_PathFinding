import heapq
import math
from grid import EMPTY, WALL, START, GOAL, VISITED, FRONTIER, PATH


# ─── Heuristics

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# ─── Reconstruct path from came_from dict

def reconstruct_path(came_from, start, goal):
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()
    return path

# ─── Greedy Best-First Search

def gbfs(grid, heuristic_fn, draw_callback=None):
    start = grid.start
    goal  = grid.goal

    # (heuristic, node)
    open_list = []
    heapq.heappush(open_list, (heuristic_fn(start, goal), start))

    came_from = {start: None}
    visited   = set()
    visited.add(start)

    nodes_visited = 0

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            path_cost = len(path) - 1
            return path, nodes_visited, path_cost

        nodes_visited += 1

        # Mark as visited
        if current != start and current != goal:
            grid.set_cell(current[0], current[1], VISITED)

        for neighbor in grid.get_neighbors(current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current

                if neighbor != goal:
                    grid.set_cell(neighbor[0], neighbor[1], FRONTIER)

                heapq.heappush(open_list, (heuristic_fn(neighbor, goal), neighbor))

        if draw_callback:
            draw_callback()

    return None, nodes_visited, 0  # No path found

# ─── A* Search

def astar(grid, heuristic_fn, draw_callback=None):
    start = grid.start
    goal  = grid.goal

    # (f, g, node)
    open_list = []
    heapq.heappush(open_list, (heuristic_fn(start, goal), 0, start))

    came_from = {start: None}
    g_cost    = {start: 0}
    expanded  = set()

    nodes_visited = 0

    while open_list:
        f, g, current = heapq.heappop(open_list)

        if current in expanded:
            continue

        expanded.add(current)

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            path_cost = g_cost[goal]
            return path, nodes_visited, path_cost

        nodes_visited += 1

        if current != start and current != goal:
            grid.set_cell(current[0], current[1], VISITED)

        for neighbor in grid.get_neighbors(current[0], current[1]):
            if neighbor in expanded:
                continue

            new_g = g_cost[current] + 1  # each step costs 1

            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor]    = new_g
                came_from[neighbor] = current
                f_val = new_g + heuristic_fn(neighbor, goal)

                if neighbor != goal:
                    grid.set_cell(neighbor[0], neighbor[1], FRONTIER)

                heapq.heappush(open_list, (f_val, new_g, neighbor))

        if draw_callback:
            draw_callback()

    return None, nodes_visited, 0  # No path found



