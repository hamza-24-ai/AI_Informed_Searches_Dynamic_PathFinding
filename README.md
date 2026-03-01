# 🚀 Dynamic Pathfinding Agent: A* vs. Greedy BFS
An interactive, grid-based pathfinding simulation developed for AI 2002 - Artificial Intelligence. This project implements informed search algorithms to navigate a grid where obstacles can appear randomly in real-time, requiring the agent to detect collisions and re-plan its path instantly.
## 🛠 Features
### Dual Algorithm Support: Toggle between A Search* (Optimal) and Greedy Best-First Search (Heuristic-only).
### Switchable Heuristics: Supports both Manhattan Distance and Euclidean Distance calculations.
### Interactive Environment: * Map Editor: Manually place or remove walls by clicking on the grid.
### Random Generation: Generate mazes with user-defined obstacle density (e.g., 30% coverage).
### Dynamic Sizing: Fully customizable grid dimensions (Rows × Columns).
### Dynamic Re-planning: New obstacles spawn while the agent is in motion. The agent detects path obstructions and re-calculates the route from its current position.

## Real-Time Visualization: Developed using Matplotlib and NumPy.

🟡 Yellow: Frontier/Open Nodes.

🔵 Blue/Red: Visited/Expanded Nodes.

🟢 Green: Final Calculated Path.


### Live Metrics: Real-time dashboard showing Nodes Visited, Path Cost, and Execution Time.

## 💻 Tech Stack
Language: Python

Logic & Grid: NumPy

GUI & Visualization: Matplotlib

Data Structures: Heapq (Priority Queue)

### 🚀 Getting Started
Prerequisites
Ensure you have Python installed. You will need the following libraries:

# Bash
pip install numpy matplotlib
Installation & Execution
Clone the repository:

## Bash
git clone https://github.com/hamza-24-ai/AI_Informed_Searches_Dynamic_PathFinding/tree/main
Navigate to the directory:

## Bash
cd your-repo-name
Run the application:

## Bash
python main.py
# 📖 How to Use
### Setup: Define your grid size and obstacle density.

### Edit: Use your mouse to click on the grid to add custom walls.


### Select: Choose your algorithm (A* or GBFS) and Heuristic (Manhattan or Euclidean) via the interface.

### Search: Watch the agent expand nodes and find the path.


Dynamic Mode: Enable dynamic obstacles to test the agent's re-planning capabilities.

## 📊 Experimental Findings
### *A Search:** Guaranteed to find the optimal (shortest) path if the heuristic is admissible.



### Greedy BFS: Faster execution and fewer nodes expanded, but often results in sub-optimal paths.


### Re-planning: By only re-calculating when the current path is blocked, the agent maintains high efficiency without resetting the entire search.

# 👨‍💻 Author

Muhammad Hamza National University of Computer & Emerging Sciences (FAST-NUCES)
