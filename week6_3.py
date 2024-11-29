import numpy as np

# Define parameters
N = 10  # Number of cities
A = 500  # Weight for enforcing one city per position
B = 500  # Weight for enforcing one position per city
C = 200  # Weight for minimizing the total distance
D = 0.01  # Weight for convergence dynamics

# Generate random distance matrix
np.random.seed(0)
distances = np.random.rand(N, N)
distances = (distances + distances.T) / 2  # Make it symmetric
np.fill_diagonal(distances, np.inf)  # No self-loops

# Initialize state and weights
state = np.random.rand(N, N)
weights = np.zeros((N, N, N, N))

# Define weights according to TSP constraints
for i in range(N):
    for j in range(N):
        for k in range(N):
            for l in range(N):
                if i == k and j != l:  # Same city, different positions
                    weights[i, j, k, l] -= A
                elif i != k and j == l:  # Same position, different cities
                    weights[i, j, k, l] -= B
                elif j == (l + 1) % N:  # Adjacent cities in the tour
                    weights[i, j, k, l] -= C * distances[i, k]

# Update function
def update_state(state, weights):
    input_signal = np.zeros_like(state)
    for i in range(N):
        for j in range(N):
            input_signal[i, j] = np.sum(weights[i, j] * state)
    new_state = 1 / (1 + np.exp(-input_signal / D))
    return new_state

# Run the network
iterations = 1000
for _ in range(iterations):
    state = update_state(state, weights)

# Decode the tour
tour = []
for j in range(N):
    city = np.argmax(state[:, j])
    tour.append(city)

# Validate the tour
if len(set(tour)) == N:
    print("Tour found:", tour)
    print("Total distance:", sum(distances[tour[i], tour[(i + 1) % N]] for i in range(N)))
else:
    print("Failed to find a valid tour")