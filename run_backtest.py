from train_hmm import RegimeHmmModel
from data_reader import DatastreamCsvPriceHandler


class Backtest(object):
    """
    Create backtest
    """

    def __init__(self, daily_prices, strategy, start_date, end_date):
        """
        Takes strategy, which defines the strategy, start date and end date of backtest
        """
        self.daily_prices = daily_prices
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date

    def _get_backtest_period(self, daily_prices, start_date, end_date):
        """
        Return backtest period
        """
        DATE = 0
        start = 0
        end = 0
        for idx, day in enumerate(daily_prices):
            # Check for starting date
            if day[DATE] == start_date:
                start = idx
            elif day[DATE] == end_date:
                end = idx
                break

        return daily_prices[start:end]

    def run(self):
        """
        Run backtest
        """
        backtest_period_daily_prices = self._get_backtest_period(self.daily_prices, self.start_date, self.end_date)
        DATE = 0
        PRICE = 1
        # Portfolio contains the date and current portfolio value
        portfolio = []
        # Check which strategy
        if self.strategy == "buy-and-hold":
            # Loop through all dates in backtest period
            for day in backtest_period_daily_prices:
                portfolio.append(day)
            return portfolio

        elif self.strategy == "regime-model":
            # TODO: 




if __name__ == "__main__":
