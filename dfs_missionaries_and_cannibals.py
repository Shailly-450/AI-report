def dfs_missionaries_and_cannibals(current_state, goal_state, visited, path, nodes_visited):
  
    nodes_visited[0] += 1

    
    if current_state == goal_state:
        return path + [goal_state], nodes_visited[0]

    
    visited.add(current_state)

    
    for next_state in generate_moves_mc(current_state):
        if next_state not in visited:
            result, nodes_visited_count = dfs_missionaries_and_cannibals(next_state, goal_state, visited, path + [current_state], nodes_visited)
            if result:
                return result, nodes_visited_count

    return None, nodes_visited[0]  

def generate_moves_mc(state):
    moves = []
    m, c, b = state  # m: missionaries, c: cannibals, b: boat position

    
    if b == 1:
       
        if m > 0:
            new_state = (m - 1, c, 0)
            if is_valid_state(new_state):
                moves.append(new_state)

       
        if c > 0:
            new_state = (m, c - 1, 0)
            if is_valid_state(new_state):
                moves.append(new_state)

       
        if m > 1:
            new_state = (m - 2, c, 0)
            if is_valid_state(new_state):
                moves.append(new_state)

       
        if c > 1:
            new_state = (m, c - 2, 0)
            if is_valid_state(new_state):
                moves.append(new_state)

        
        if m > 0 and c > 0:
            new_state = (m - 1, c - 1, 0)
            if is_valid_state(new_state):
                moves.append(new_state)

   
    else:
        
        if m < 3:
            new_state = (m + 1, c, 1)
            if is_valid_state(new_state):
                moves.append(new_state)

        
        if c < 3:
            new_state = (m, c + 1, 1)
            if is_valid_state(new_state):
                moves.append(new_state)

       
        if m < 2:
            new_state = (m + 2, c, 1)
            if is_valid_state(new_state):
                moves.append(new_state)

       
        if c < 2:
            new_state = (m, c + 2, 1)
            if is_valid_state(new_state):
                moves.append(new_state)

        
        if m < 3 and c < 3:
            new_state = (m + 1, c + 1, 1)
            if is_valid_state(new_state):
                moves.append(new_state)

    return moves

def is_valid_state(state):
    m, c, _ = state
    
    if (m >= c or m == 0) and ((3 - m) >= (3 - c) or (3 - m) == 0):
        return True
    return False


initial_state = (3, 3, 1)  # 3 missionaries, 3 cannibals, boat on the original side
goal_state = (0, 0, 0)  # All missionaries and cannibals on the opposite side


visited = set()
nodes_visited = [0] 
solution_path, total_nodes_visited = dfs_missionaries_and_cannibals(initial_state, goal_state, visited, [], nodes_visited)


if solution_path:
    print("Solution found! The sequence of steps is:")
    for step in solution_path:
        print(step)
    print(f"Total Number of nodes visited: {total_nodes_visited}")
else:
    print("No solution found.")
    print(f"Total Number of nodes visited: {total_nodes_visited}")