import copy

directions = {'up': (-1,0), 'down': (1,0), 'left': (0,-1), 'right': (0,1)}

def manhattan_distance(state, goal):
    distance = 0
    pos_goal = {}
    for i in range(3):
        for j in range(3):
            pos_goal[goal[i][j]] = (i,j)
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                gi, gj = pos_goal[val]
                distance += abs(i - gi) + abs(j - gj)
    return distance

def get_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def move(state, direction):
    i, j = get_blank(state)
    di, dj = directions[direction]
    ni, nj = i + di, j + dj
    if 0 <= ni < 3 and 0 <= nj < 3:
        new_state = copy.deepcopy(state)
        new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
        return new_state
    return None

def print_state(state):
    for row in state:
        print(' '.join(str(x) for x in row))
    print()

def hill_climb(start, goal):
    current = start
    current_h = manhattan_distance(current, goal)
    path = []
    print("Start State:")
    print_state(current)
    while True:
        neighbors = []
        for move_dir in directions:
            new_state = move(current, move_dir)
            if new_state:
                h = manhattan_distance(new_state, goal)
                neighbors.append((h, new_state, move_dir))
        neighbors.sort()
        if neighbors and neighbors[0][0] < current_h:
            current_h = neighbors[0][0]
            current = neighbors[0][1]
            move_made = neighbors[0][2]
            path.append(move_made)
            print(f"Move: {move_made}")
            print_state(current)
            if current == goal:
                return path
        else:
            return path

print("Enter the start state row by row (use 0 for blank):")
start_state = [list(map(int, input().split())) for _ in range(3)]

print("Enter the goal state row by row (use 0 for blank):")
goal_state = [list(map(int, input().split())) for _ in range(3)]

solution = hill_climb(start_state, goal_state)
print("Sequence of moves:", solution)
