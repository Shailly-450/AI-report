def dfs_rabbit_leap(current_state, goal_state, visited, path):
    
    if current_state == goal_state:
        return path + [goal_state]

    
    visited.add(current_state)

    
    for next_state in generate_moves(current_state):
        if next_state not in visited:
            result = dfs_rabbit_leap(next_state, goal_state, visited, path + [current_state])
            if result:
                return result

    return None 

def generate_moves(state):
    moves = []
    index = state.index('X')

   
    if index > 0:
        new_state = list(state)
        new_state[index], new_state[index - 1] = new_state[index - 1], new_state[index]
        moves.append(''.join(new_state))

    
    if index < len(state) - 1:
        new_state = list(state)
        new_state[index], new_state[index + 1] = new_state[index + 1], new_state[index]
        moves.append(''.join(new_state))

    
    if index > 1:
        new_state = list(state)
        new_state[index], new_state[index - 2] = new_state[index - 2], new_state[index]
        moves.append(''.join(new_state))

    
    if index < len(state) - 2:
        new_state = list(state)
        new_state[index], new_state[index + 2] = new_state[index + 2], new_state[index]
        moves.append(''.join(new_state))

    return moves

# Initial and goal states
initial_state = "EEEXWWW"
goal_state = "WWWXEEE"


visited = set()
solution_path = dfs_rabbit_leap(initial_state, goal_state, visited, [])


if solution_path:
    print("Solution found! The sequence of steps is:")
    for step in solution_path:
        print(step)
else:
    print("No solution found.")