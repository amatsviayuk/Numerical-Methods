import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calculate_ema(price, n):
    a = 2 / (n + 1)
    ema = np.zeros(len(price))
    ema[0] = price[0]

    for i in range(1, len(price)):  # formula (1)
        ema[i] = (price[i] + (1 - a) * ema[i - 1]) / (1 + (1 - a))

    return ema


def calculate_signal(mcd, n):
    sign = calculate_ema(mcd, n)  # EMA 9
    return sign


def execute_trades(prices, transactions, capital):
    shares = capital / prices[0]  # Initial number of stocks
    capital = 0

    for transaction in transactions:
        action, price, day = transaction
        if action == 'Buy':
            shares_to_buy = capital / price
            shares += shares_to_buy
            capital -= shares_to_buy * price
        elif action == 'Sell':
            capital += shares * price
            shares = 0

    return capital


def simulate_trading(prices, macd, signal, initial_capital=1000):
    capital = initial_capital
    transactions = []
    profitable_transactions = []
    unprofitable_transactions = []

    for i in range(1, len(prices)):
        if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]:  # Buy(MACD > Signal, MACD++)
            capital -= prices[i]
            transactions.append(('Buy', prices[i], i))
        elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:  # Sell(MACD < Signal, MACD--)
            capital += prices[i]
            transactions.append(('Sell', prices[i], i))

    # Calculating the profit
    for transaction in transactions:  # trading
        action, price, day = transaction
        if action == 'Buy':
            # Searching for next Sell in transactions
            next_sell = next((t for t in transactions[transactions.index(transaction) + 1:] if t[0] == 'Sell'), None)
            if next_sell:  # If the condition above was found, calculating the profit
                profit = next_sell[1] - price
                if profit > 0:  # Adding the transaction to suitable group
                    profitable_transactions.append((day, profit))
                else:
                    unprofitable_transactions.append((day, profit))

    # Calculating final capital
    final_capital = execute_trades(prices, transactions, initial_capital)

    # Stats output
    for transaction in transactions:
        print(transaction[0], 'at price:', transaction[1], 'on day', transaction[2])
    print('Final capital:', final_capital)

    # Profit/Loss at a specific day
    print('Profitable transactions:')
    for day, profit in profitable_transactions:
        print('Day:', day, 'Profit:', profit)
    print('Unprofitable transactions:')
    for day, loss in unprofitable_transactions:
        print('Day:', day, 'Loss:', loss)

    # Was it profitable?
    if final_capital > initial_capital:
        print("Using MACD was profitable.")
    else:
        print("Using MACD was not profitable.")

    print("Initial capital: ", initial_capital)
    print("Final capital: ", final_capital)


all_data = pd.read_csv('eurpln.csv')  # getting data
prices = all_data['Zamkniecie'].values[:1000]

# Calculating EMA12 and EMA16. Calculating signal for 9
ema_12 = calculate_ema(prices, 12)
ema_26 = calculate_ema(prices, 26)
macd = ema_12 - ema_26
signal = calculate_signal(macd, 9)


# Initial chart
plt.figure(figsize=(10, 6))
plt.plot(np.arange(len(prices)), prices, label='Closing Price')
plt.title('Price chart for EUR/PLN for 1000 days')
plt.xlabel('Days')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

x = np.arange(0, 1000)

#  MACD and Signal
plt.figure(figsize=(10, 6))
plt.title('MACD and Signal')
plt.plot(np.arange(len(prices)), macd, label='MACD')
plt.plot(np.arange(len(prices)), signal, label='Signal')

buy_signals = []
sell_signals = []
intersection_points = []

for i in range(1, len(macd)):  # Adding Buy/Sell points
    if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]:
        buy_signals.append(i)
        intersection_points.append((x[i], macd[i]))
    elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
        sell_signals.append(i)
        intersection_points.append((x[i], macd[i]))

buy_x, buy_y = zip(*intersection_points)
plt.scatter(buy_x, buy_y, color='blue', marker='o', label='Intersection Points')

plt.scatter(buy_signals, macd[buy_signals], color='green', marker='^', label='Buy Signal')
plt.scatter(sell_signals, macd[sell_signals], color='red', marker='v', label='Sell Signal')

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()


def generate_signals(macd, signal_line):
    signals = np.zeros(len(macd))
    for i in range(1, len(macd)):
        if macd[i] > signal_line[i] and macd[i - 1] <= signal_line[i - 1]:
            signals[i] = 1  # Buy Signal
        elif macd[i] < signal_line[i] and macd[i - 1] >= signal_line[i - 1]:
            signals[i] = -1  # Sell Signal
    return signals


signals = generate_signals(macd, signal)

# Buy/Sell points chart
plt.figure(figsize=(10, 6))
plt.plot(np.arange(len(prices)), prices, label='Closing Price', color='black')
plt.scatter(np.where(signals == 1)[0], prices[signals == 1], marker='^', color='g', label='Buy')
plt.scatter(np.where(signals == -1)[0], prices[signals == -1], marker='v', color='r', label='Sell')
plt.title('Buy/Sell points chart')
plt.xlabel('Days')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

#simulate_trading(prices, macd, signal, initial_capital=1000)

def improve_macd_trading(prices, macd, signal, initial_capital=1000):
    capital = initial_capital
    transactions = []
    profitable_transactions = []
    unprofitable_transactions = []

    # Additional state
    for i in range(1, len(prices)):
        if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1] and macd[i] > 0:  # MACD > 0
            capital -= prices[i]
            transactions.append(('Buy', prices[i], i))
        elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1] and macd[i] < 0:  # MACD < 0
            capital += prices[i]
            transactions.append(('Sell', prices[i], i))

    # Calculate the profit
    for transaction in transactions:
        action, price, day = transaction
        if action == 'Buy':
            next_sell = next((t for t in transactions[transactions.index(transaction) + 1:] if t[0] == 'Sell'), None)
            if next_sell:
                profit = next_sell[1] - price
                if profit > 0:
                    profitable_transactions.append((day, profit))
                else:
                    unprofitable_transactions.append((day, profit))

    # Calculating final capital
    final_capital = execute_trades(prices, transactions, initial_capital)

    # Stats
    for transaction in transactions:
        print(transaction[0], 'at price:', transaction[1], 'on day', transaction[2])
    print('Final capital:', final_capital)

    # Profit output
    print('Profitable transactions:')
    for day, profit in profitable_transactions:
        print('Day:', day, 'Profit:', profit)
    print('Unprofitable transactions:')
    for day, loss in unprofitable_transactions:
        print('Day:', day, 'Loss:', loss)

    # Profit?
    if final_capital > initial_capital:
        print("Using improved MACD trading strategy was profitable.")
    else:
        print("Using improved MACD trading strategy was not profitable.")

    print("Initial capital: ", initial_capital)
    print("Final capital: ", final_capital)


improve_macd_trading(prices, macd, signal, initial_capital=1000)

