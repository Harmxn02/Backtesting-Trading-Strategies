from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG
import numpy as np
import matplotlib.pyplot as plt

class MACD_Strategy(Strategy):
    def init(self):
        price = self.data.Close
        self.short_window = 12
        self.long_window = 26
        self.signal_window = 9

        # Calculate MACD components
        self.macd_line = self.calculate_rolling_mean(price, window=self.short_window) \
                         - self.calculate_rolling_mean(price, window=self.long_window)
        self.signal_line = self.calculate_rolling_mean(self.macd_line, window=self.signal_window)
        self.macd_histogram = self.macd_line - self.signal_line

    def calculate_rolling_mean(self, series, window):
        rolling_means = []
        for i in range(len(series)):
            start_index = max(0, i - window + 1)
            current_mean = np.mean(series[start_index:i + 1])
            rolling_means.append(current_mean)
        return np.array(rolling_means)

    def next(self):
        if crossover(self.macd_line, self.signal_line):
            self.buy()
        elif crossover(self.signal_line, self.macd_line):
            self.sell()

# Create Backtest instance
bt = Backtest(GOOG, MACD_Strategy, commission=.002, exclusive_orders=True)
bt.run()
