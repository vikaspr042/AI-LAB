import math

# Alpha-Beta Pruning function
def alpha_beta(depth, node_index, maximizing_player, values, alpha, beta, max_depth, path):
    indent = "  " * depth  # for clear step indentation
    if depth == max_depth:
        print(f"{indent}Reached leaf node {values[node_index]} (Depth {depth})")
        return values[node_index]

    if maximizing_player:
        print(f"{indent}MAX node at depth {depth}, alpha={alpha}, beta={beta}")
        max_eval = -math.inf
        for i in range(2):  # assuming binary tree
            value = alpha_beta(depth + 1, node_index * 2 + i, False,
                               values, alpha, beta, max_depth, path)
            print(f"{indent}MAX node considers child {node_index * 2 + i} → value={value}")
            max_eval = max(max_eval, value)
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                print(f"{indent}Pruned remaining branches at MAX node (alpha={alpha}, beta={beta})")
                break  # beta cut-off
        return max_eval

    else:
        print(f"{indent}MIN node at depth {depth}, alpha={alpha}, beta={beta}")
        min_eval = math.inf
        for i in range(2):
            value = alpha_beta(depth + 1, node_index * 2 + i, True,
                               values, alpha, beta, max_depth, path)
            print(f"{indent}MIN node considers child {node_index * 2 + i} → value={value}")
            min_eval = min(min_eval, value)
            beta = min(beta, min_eval)
            if beta <= alpha:
                print(f"{indent}Pruned remaining branches at MIN node (alpha={alpha}, beta={beta})")
                break  # alpha cut-off
        return min_eval


# Example game tree leaf values
values = [3, 5, 6, 9, 1, 2, 0, -1]
max_depth = 3

print("===== Alpha-Beta Pruning Trace =====\n")
best_value = alpha_beta(0, 0, True, values, -math.inf, math.inf, max_depth, [])
print("\n===== Final Result =====")
print(f"Value of the root node (Optimal value): {best_value}")
print("===================================")
