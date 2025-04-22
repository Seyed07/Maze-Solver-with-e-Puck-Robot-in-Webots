# Maze Solver with e‑Puck Robot

## 🚀 Project Overview
This repository demonstrates pathfinding in a 4×4 maze using an e‑Puck robot in the Webots simulator. The robot uses infrared proximity sensors to detect walls and performs a depth‑first search (DFS) with a stack to navigate from the start cell (ID 3) to the center of the maze.

## 📋 Repository Structure
```
maze-solver-epuck/
├── controllers/
│   └── my_controller.py      # Robot controller implementation
├── worlds/
│   └── maze.wbt            # Maze world file for Webots
├── README.md               # This file
└── requirements.txt        # Python dependencies (if any)
```

## 🔧 Prerequisites
- **Python 3.8+**
- **Webots 2023b** or later
- **Webots Python API** (included with Webots installation)

## 📥 Installation
```bash
# Clone the repository
git clone https://github.com/<username>/maze-solver-epuck.git
cd maze-solver-epuck
```

## ▶️ Running the Simulation
1. Launch Webots.
2. Open the world file: **File → Open World → worlds/maze.wbt**.
3. In the Robot Controller panel, select `my_controller.py`.
4. Press the ▶️ Run button to start the simulation.

## ⚙️ Sensor and Motor Configuration
```python
# Infrared proximity sensors: front, right, rear, left
psNames = ['ps0', 'ps7', 'ps3', 'ps4']
threshold = 80  # sensor reading above this indicates a wall

# Configure wheel motors for infinite rotation and zero speed initially
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)
```

## 🧠 DFS Algorithm with Stack
The core algorithm is an iterative Depth‑First Search (DFS) maintained with a stack:
1. **Node Representation**: Each cell is a `node` object with attributes: `id`, `dir` (entry orientation), and `searched` (boolean).
2. **Stack Usage**: The stack holds the current path and candidate nodes.
3. **Initialization**:
   ```python
   stack = []
   stack.append(start_node)  # push starting node (ID 3)
   ```
4. **Search Loop**:
   ```python
   while stack:
       current = stack[-1]  # peek top
       if not current.searched:
           stack = search(current, stack, duration)  # explore neighbors
       else:
           stack.pop()  # backtrack
   ```
- When exploring a node, the `search()` function reads sensor data, identifies free directions in priority order (right → forward → left), updates the graph edges, and pushes new nodes onto the stack.  
- If no unvisited neighbors are found, two `pop()` operations backtrack the robot physically.

### Recursive DFS Example
```python
visited = set()

def dfs_recursive(node):
    visited.add(node)
    if node == goal:
        return True
    for direction in ['right', 'forward', 'left']:
        if is_free(direction):
            nxt = move(direction)
            if nxt not in visited and dfs_recursive(nxt):
                return True
            backtrack()
    return False

# Start search
dfs_recursive(start_node)
```

## ⚠️ Known Issues
- **Return Path Accuracy**: Final calibration errors in `delay()` cause slight deviations on the return journey.
- **Delay Tuning**: The `delay()` durations in rotation functions may require manual adjustment for precise turns.

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for:
- Optimizing sensor processing
- Improving motor calibration
- Refactoring code for readability


---
*For questions or feedback, please raise an issue or contact via email.*

