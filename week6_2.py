import numpy as np

class HopfieldEightRook:
    def __init__(self, size=8):
        self.size = size  # Size of the chessboard (8x8)
        self.num_neurons = size * size
        self.weights = np.zeros((self.num_neurons, self.num_neurons))  # Weight matrix
        self.initialize_weights()

    def initialize_weights(self):
        """Initialize weights for the Hopfield network based on Eight-Rook constraints."""
        for i in range(self.size):
            for j in range(self.size):
                neuron_index = i * self.size + j
                for k in range(self.size):
                    # Row constraints
                    if k != j:
                        self.weights[neuron_index, i * self.size + k] = -1
                    # Column constraints
                    if k != i:
                        self.weights[neuron_index, k * self.size + j] = -1
        np.fill_diagonal(self.weights, 0)  # No self-connections

    def energy(self, state):
        """Calculate the energy of the current state."""
        return -0.5 * np.dot(state, np.dot(self.weights, state))

    def step(self, state):
        """Update the state of the network asynchronously."""
        for _ in range(self.num_neurons):
            neuron = np.random.randint(0, self.num_neurons)
            activation = np.dot(self.weights[neuron], state)
            state[neuron] = 1 if activation > 0 else 0
        return state

    def solve(self, max_iter=1000):
        """Solve the Eight-Rook problem using the Hopfield network."""
        state = np.random.choice([0, 1], size=self.num_neurons)  # Random initial state
        for _ in range(max_iter):
            previous_state = state.copy()
            state = self.step(state)
            if np.array_equal(state, previous_state):
                break
        return state.reshape(self.size, self.size)

def main():
    size = 8
    hopfield = HopfieldEightRook(size)
    solution = hopfield.solve()

    # Display solution
    print("Eight-Rook Solution:")
    for row in solution:
        print(" ".join("R" if cell else "." for cell in row))

if __name__ == "__main__":
    main()
