import numpy as np
class ModifiedEpsilonGreedy:
    def _init_(self, bandit, epsilon=0.1, alpha=0.1):
        self.bandit = bandit
        self.epsilon = epsilon  # Exploration probability
        self.alpha = alpha  # Step-size for updating action-value estimates
        self.action_values = np.zeros(10)  # Initialize action-value estimates

    def select_action(self):
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, 10)  # Explore
        else:
            return np.argmax(self.action_values)  # Exploit

    def update_estimates(self, action, reward):
        # Update action-value estimates using constant step-size alpha
        self.action_values[action] += self.alpha * (reward - self.action_values[action])

    def run(self, time_steps):
        rewards = np.zeros(time_steps)
        optimal_action_count = np.zeros(time_steps)

        for t in range(time_steps):
            action = self.select_action()
            reward = self.bandit.bandit_nonstat(action)
            rewards[t] = reward
            self.update_estimates(action, reward)

            optimal_action = np.argmax(self.bandit.mean_rewards)
            if action == optimal_action:
                optimal_action_count[t] = 1

            self.bandit.update_means()
        
        return rewards, optimal_action_count
