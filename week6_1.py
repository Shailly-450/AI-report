import numpy as np

class HopfieldNetwork:
    def __init__(self, num_neurons):
        self.num_neurons = num_neurons
        self.weights = np.zeros((num_neurons, num_neurons))

    def train(self, patterns):
        """Train the Hopfield network using Hebbian learning."""
        for pattern in patterns:
            pattern = pattern.reshape(-1, 1)
            self.weights += pattern @ pattern.T
        np.fill_diagonal(self.weights, 0)  # No self-connections

    def recall(self, pattern, max_iter=10):
        """Recall a pattern, iterating until convergence or max_iter."""
        output = pattern.copy()
        for _ in range(max_iter):
            prev_output = output.copy()
            output = np.sign(self.weights @ output)
            output[output == 0] = 1  # Resolve ties to 1
            if np.array_equal(output, prev_output):
                break
        return output

    def introduce_noise(self, pattern, noise_level):
        """Flip a given percentage of bits in the pattern."""
        noisy_pattern = pattern.copy()
        num_flips = int(len(pattern) * noise_level)
        flip_indices = np.random.choice(len(pattern), num_flips, replace=False)
        noisy_pattern[flip_indices] *= -1
        return noisy_pattern

def generate_patterns(num_patterns, num_neurons):
    """Generate random binary patterns (+1/-1)."""
    return np.random.choice([-1, 1], size=(num_patterns, num_neurons))

def test_hopfield_network():
    num_neurons = 100
    num_patterns = 10
    noise_levels = [0.1, 0.2, 0.3, 0.4, 0.5]

    # Create and train the Hopfield network
    hopfield_net = HopfieldNetwork(num_neurons)
    patterns = generate_patterns(num_patterns, num_neurons)
    hopfield_net.train(patterns)

    # Test the network's error-correcting capability
    for i, pattern in enumerate(patterns):
        print(f"\nPattern {i + 1}:")
        for noise_level in noise_levels:
            noisy_pattern = hopfield_net.introduce_noise(pattern, noise_level)
            recalled_pattern = hopfield_net.recall(noisy_pattern)
            accuracy = np.mean(recalled_pattern == pattern)
            print(f"Noise Level: {noise_level * 100:.0f}%, Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    test_hopfield_network()
