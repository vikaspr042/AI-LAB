def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def swap(state, x1, y1, x2, y2):
    new_state = [row[:] for row in state]
    new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
    return new_state

def dfs(state, goal, path, visited):
    if state == goal:
        return path + [state]

    visited.add(str(state))
    x, y = find_zero(state)

    moves = [(-1,0), (1,0), (0,-1), (0,1)]  # Up, Down, Left, Right

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = swap(state, x, y, nx, ny)
            if str(new_state) not in visited:
                result = dfs(new_state, goal, path + [state], visited)
                if result is not None:
                    return result
    return None

def input_state(prompt):
    print(prompt)
    state = []
    for _ in range(3):
        row = input("Enter 3 numbers separated by spaces (use 0 for blank): ").split()
        row = list(map(int, row))
        state.append(row)
    return state

def print_board(board):
    for row in board:
        print(' '.join(str(x) if x != 0 else ' ' for x in row))
    print()

if __name__ == "__main__":
    start = input_state("Enter START state:")
    goal = input_state("Enter GOAL state:")

    print("\nSearching for solution with pure DFS (no depth limit)...")

    solution = dfs(start, goal, [], set())

    if solution:
        print(f"\nSolution found in {len(solution)-1} moves:\n")
        for step, board in enumerate(solution):
            print(f"Step {step}:")
            print_board(board)
    else:
        print("\nNo solution found.")
