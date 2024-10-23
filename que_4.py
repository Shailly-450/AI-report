import numpy as np

class TenArmedBandit:
    def _init_(self):
        self.mean_rewards = np.zeros(10)  # Initialize mean rewards for 10 arms
        self.action_counts = np.zeros(10)  # Track action counts

    def bandit_nonstat(self, action):
        # Generate reward based on current mean reward for the selected action
        reward = np.random.normal(self.mean_rewards[action], 1.0)
        return reward

    def update_means(self):
        # Update mean rewards with small random Gaussian increments
        self.mean_rewards += np.random.normal(0, 0.01, 10)
