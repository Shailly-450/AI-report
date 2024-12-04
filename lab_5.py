import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Data Acquisition
ticker = "TSLA"
data = yf.download(ticker, start="2013-01-01", end="2023-12-31")
data['Returns'] = data['Adj Close'].pct_change().dropna()

# Preprocessing
data = data.dropna()
returns = data['Returns'].values.reshape(-1, 1)
from hmmlearn.hmm import GaussianHMM

# Fit HMM with 2 hidden states
model = GaussianHMM(n_components=2, covariance_type="full", n_iter=1000)
model.fit(returns)

# Decode hidden states
hidden_states = model.predict(returns)

# Extract model parameters
means = model.means_
variances = np.sqrt(np.array([cov.diagonal() for cov in model.covars_]))
transition_matrix = model.transmat_

print("Means:", means)
print("Variances:", variances)
print("Transition Matrix:\n", transition_matrix)

# Plot stock prices and hidden states
plt.figure(figsize=(12, 6))
for i, state in enumerate(np.unique(hidden_states)):
    plt.plot(data.index[hidden_states == state], 
             data['Adj Close'][hidden_states == state], 
             '.', label=f'State {i}')
plt.title(f"Hidden States for {ticker}")
plt.xlabel("Date")
plt.ylabel("Adjusted Close Price")
plt.legend()
plt.show()

# Plot transition matrix
import seaborn as sns
sns.heatmap(transition_matrix, annot=True, cmap="Blues")
plt.title("Transition Matrix")
plt.xlabel("From State")
plt.ylabel("To State")
plt.show()
