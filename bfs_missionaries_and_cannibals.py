from collections import deque

def bfs_missionaries_and_cannibals(initial_state, goal_state):
    
    queue = deque([(initial_state, [])])
    visited = set() 
    nodes_visited = 0  

    while queue:
        current_state, path = queue.popleft()

        
        nodes_visited += 1

        
        if current_state == goal_state:
            return path + [goal_state], nodes_visited

        
        visited.add(current_state)

        
        for next_state in generate_moves_mc(current_state):
            if next_state not in visited:
                queue.append((next_state, path + [current_state]))

    return None, nodes_visited 

def generate_moves_mc(state):
    moves = []
    m, c, b = state  

   
    if b == 1:
        # Move 1 missionary
        if m > 0:
            new_state = (m - 1, c, 0)
            if is_valid_state(new_state):
                moves.append(new_state)

        # Move 1 cannibal
        if c > 0:
            new_state = (m, c - 1, 0)
            if is_valid_state(new_state):
                moves.append(new_state)

        # Move 2 missionaries
        if m > 1:
            new_state = (m - 2, c, 0)
            if is_valid_state(new_state):
                moves.append(new_state)

        # Move 2 cannibals
        if c > 1:
            new_state = (m, c - 2, 0)
            if is_valid_state(new_state):
                moves.append(new_state)

        # Move 1 missionary and 1 cannibal
        if m > 0 and c > 0:
            new_state = (m - 1, c - 1, 0)
            if is_valid_state(new_state):
                moves.append(new_state)

    
    else:
        # Move 1 missionary
        if m < 3:
            new_state = (m + 1, c, 1)
            if is_valid_state(new_state):
                moves.append(new_state)

        # Move 1 cannibal
        if c < 3:
            new_state = (m, c + 1, 1)
            if is_valid_state(new_state):
                moves.append(new_state)

        # Move 2 missionaries
        if m < 2:
            new_state = (m + 2, c, 1)
            if is_valid_state(new_state):
                moves.append(new_state)

        # Move 2 cannibals
        if c < 2:
            new_state = (m, c + 2, 1)
            if is_valid_state(new_state):
                moves.append(new_state)

        # Move 1 missionary and 1 cannibal
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

# Initial and goal states
initial_state = (3, 3, 1)  # 3 missionaries, 3 cannibals, boat on the original side
goal_state = (0, 0, 0)  # All missionaries and cannibals on the opposite side


solution_path, nodes_visited = bfs_missionaries_and_cannibals(initial_state, goal_state)


if solution_path:
    print("Solution found! The sequence of steps is:")
    for step in solution_path:
        print(step)
    print(f"Total Number of nodes visited: {nodes_visited}")
else:
    print("No solution found.")
    print(f"Total Number of nodes visited: {nodes_visited}")