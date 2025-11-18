import heapq

# ----- Goal state -----
goal_state = [[1, 2, 3],
              [8, 0, 4],
              [7, 6, 5]]

# ----- Moves (up, down, left, right) -----
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Precompute goal positions for Manhattan distance
goal_positions = {}
for i in range(3):
    for j in range(3):
        goal_positions[goal_state[i][j]] = (i, j)

# ----- Heuristic Function -----
def manhattan_distance(state):
    """Calculate the Manhattan distance heuristic."""
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                gi, gj = goal_positions[value]
                distance += abs(i - gi) + abs(j - gj)
    return distance

# ----- Utility Functions -----
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def print_state(state):
    for row in state:
        print(" ".join(str(x) if x != 0 else " " for x in row))
    print()

# ----- A* Search -----
def a_star(start_state):
    open_set = []
    heapq.heappush(open_set, (0, start_state, [], 0))  # (f, state, path, g)
    visited = set()

    print("🔹 Starting A* Search...\n")
    while open_set:
        f, current, path, g = heapq.heappop(open_set)
        if state_to_tuple(current) in visited:
            continue
        visited.add(state_to_tuple(current))

        h = manhattan_distance(current)
        print(f"Exploring Node (g={g}, h={h}, f={f}):")
        print_state(current)

        if current == goal_state:
            print("✅ Goal Reached!\n")
            return path + [current]

        for neighbor in get_neighbors(current):
            if state_to_tuple(neighbor) not in visited:
                g_new = g + 1
                h_new = manhattan_distance(neighbor)
                f_new = g_new + h_new
                heapq.heappush(open_set, (f_new, neighbor, path + [current], g_new))

    return None

# ----- Example Input -----
initial_state = [[2, 8, 3],
                 [1, 6, 4],
                 [7, 0, 5]]

print("🔹 Initial State:")
print_state(initial_state)
print("🔹 Goal State:")
print_state(goal_state)

solution = a_star(initial_state)

# ----- Print Solution Path -----
if solution:
    print("🔹 Solution Path:")
    for step, state in enumerate(solution):
        g = step
        h = manhattan_distance(state)
        f = g + h
        print(f"Step {step}: g={g}, h={h}, f={f}")
        print_state(state)
else:
    print("❌ No solution found.")
