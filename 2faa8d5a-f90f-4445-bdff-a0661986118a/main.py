from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initializing with a single ticker for simplicity
        self.tickers = ["TSLA"]
        # No additional data requirements declared
        self.data_list = []

    @property
    def interval(self):
        # Using daily interval for MACD analysis
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # No initial allocation; dynamically allocated based on MACD indicator
        allocation_dict = {ticker: 0 for ticker in self.tickers}

        # Running MACD with standard parameters; fast = 12, slow = 26
        macd_data = MACD("TSLA", data["ohlcv"], fast=12, slow=26)

        # Check if MACD and Signal data has been populated properly
        if macd_data and len(macd_data["MACD"]) > 1:
            current_macd = macd_data["MACD"][-1]
            previous_macd = macd_data["MACD"][-2]
            current_signal = macd_data["signal"][-1]
            previous_signal = macd_data["signal"][-2]

            # Generate Buy signal (allocation 100%) if MACD crosses above Signal
            if current_macd > current_signal and previous_macd <= previous_signal:
                log("BUY signal for TSLA")
                allocation_dict["TSLA"] = 1.0
            # Generate Sell signal (allocation 0%) if MACD crosses below Signal
            elif current_macd < current_signal and previous_macd >= previous_signal:
                log("SELL signal for TSLA")
                allocation_dict["TSLA"] = 0.0
            else:
                # No trade signal; maintain current allocation
                log("No trade signal for TSLA")

        # Returns a TargetAllocation object to adjust portfolios according to signals
        return TargetAllocation(allocation_dict)