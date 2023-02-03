import yfinance as yf
import pandas as pd

# Get the S&P 500 companies and save them to a CSV file
table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
df.to_csv('S&P500-Info.csv')
df.to_csv("S&P500-Symbols.csv", columns=['Symbol'])

# Get the data for the S&P 500 companies from the CSV
tickers = yf.Tickers(' '.join(df['Symbol'].to_list()))

# Clean the data for stocks that are not available
tickers.tickers.pop('BRK.B', None)
tickers.tickers.pop('BF.B', None)

# Initialize the buy and sell lists
buy_list = []
sell_list = []

print("Calculating recommendations...")

# Loop through the tickers and calculate the 50 day and 200 day moving averages
for ticker in tickers.tickers:
    fifty = tickers.tickers[ticker].history(period="50d")['Close'].mean()
    two_hundred = tickers.tickers[ticker].history(period="200d")['Close'].mean()
    indicator = fifty - two_hundred
    # Buy (or hold) the stock if the 50 day moving average is greater than the 200 day moving average
    if indicator < 0:
        buy_list.append(ticker)
    # Sell the stock if the 50 day moving average is less than the 200 day moving average
    elif indicator > 0:
        sell_list.append(ticker)

print("Recommendations complete!")

# Print the buy and sell lists
print("Number of stocks to buy: " + str(len(buy_list)))
print("Number of stocks to sell: " + str(len(sell_list)))
print("Buy List:")
print(buy_list)
print("Sell List:")
print(sell_list)
