import numpy as np  # Make sure to import numpy

# Initialize a matchbox for a specific game state
matchbox = {'---|---|---': [3, 3, 3, 3, 3, 3, 3, 3, 3]}  # Example for an empty board

# Choose a move based on bead distribution
def select_move(state):
    moves = matchbox[state]
    total_beads = sum(moves)
    probabilities = [move / total_beads for move in moves]
    return np.random.choice(range(9), p=probabilities)

# Update beads based on game outcome
def update_beads(state, move, result):
    if result == 'win':
        matchbox[state][move] += 1
    elif result == 'loss':
        matchbox[state][move] = max(0, matchbox[state][move] - 1)  # Penalize for a loss
