import heapq
import math
from grid import START, GOAL, VISITED, FRONTIER, PATH


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def reconstruct_path(came_from, start, goal):
    path, node = [], goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()
    return path


def gbfs(grid, heuristic_fn, draw_callback=None):
    start, goal   = grid.start, grid.goal
    open_list     = [(heuristic_fn(start, goal), start)]
    came_from     = {start: None}
    visited       = {start}
    nodes_visited = 0

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            return path, nodes_visited, len(path) - 1

        nodes_visited += 1
        if current != start and current != goal:
            grid.set_cell(current[0], current[1], VISITED)

        for nb in grid.get_neighbors(current[0], current[1]):
            if nb not in visited:
                visited.add(nb)
                came_from[nb] = current
                if nb != goal:
                    grid.set_cell(nb[0], nb[1], FRONTIER)
                heapq.heappush(open_list, (heuristic_fn(nb, goal), nb))

        if draw_callback:
            draw_callback()

    return None, nodes_visited, 0


def astar(grid, heuristic_fn, draw_callback=None):
    start, goal   = grid.start, grid.goal
    open_list     = [(heuristic_fn(start, goal), 0, start)]
    came_from     = {start: None}
    g_cost        = {start: 0}
    expanded      = set()
    nodes_visited = 0

    while open_list:
        f, g, current = heapq.heappop(open_list)

        if current in expanded:
            continue
        expanded.add(current)

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            return path, nodes_visited, g_cost[goal]

        nodes_visited += 1
        if current != start and current != goal:
            grid.set_cell(current[0], current[1], VISITED)

        for nb in grid.get_neighbors(current[0], current[1]):
            if nb in expanded:
                continue
            new_g = g_cost[current] + 1
            if nb not in g_cost or new_g < g_cost[nb]:
                g_cost[nb]    = new_g
                came_from[nb] = current
                if nb != goal:
                    grid.set_cell(nb[0], nb[1], FRONTIER)
                heapq.heappush(open_list, (new_g + heuristic_fn(nb, goal), new_g, nb))

        if draw_callback:
            draw_callback()

    return None, nodes_visited, 0


def mark_path(grid, path):
    for node in path:
        if node != grid.start and node != grid.goal:
            grid.set_cell(node[0], node[1], PATH)