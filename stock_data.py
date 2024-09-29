import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM

def download_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def fit_hmm(returns, n_states=2):
    model = GaussianHMM(n_components=n_states, covariance_type="full", n_iter=1000)
    model.fit(returns.reshape(-1, 1))
    hidden_states = model.predict(returns.reshape(-1, 1))
    return model, hidden_states

start_date = "2013-01-01"
end_date = "2023-01-01"
ticker = "AAPL" 
stock_data = download_stock_data(ticker, start_date, end_date)
stock_data['Return'] = stock_data['Adj Close'].pct_change().dropna()
stock_data = stock_data.dropna()

model, hidden_states = fit_hmm(stock_data['Return'].values)
stock_data['Hidden_State'] = hidden_states

plt.figure(figsize=(14, 8))
for i in range(model.n_components):
    state = stock_data[stock_data['Hidden_State'] == i]
    plt.scatter(state.index, state['Return'], label=f'State {i}', alpha=0.6)
plt.title(f'Returns of {ticker} with Hidden States')
plt.xlabel('Date')
plt.ylabel('Return')
plt.legend()
plt.show()

print("Transition Matrix:")
print(model.transmat_)