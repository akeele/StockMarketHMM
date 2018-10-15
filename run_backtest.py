from train_hmm import RegimeHmmModel
from data_reader import DatastreamCsvPriceHandler


class Backtest(object):
    """
    Create backtest
    """

    def __init__(self, daily_prices, strategy, hmm_model, start_date, end_date):
        """
        Takes strategy, which defines the strategy, start date and end date of backtest
        """
        self.daily_prices = daily_prices
        self.strategy = strategy
        self.strategy = hmm_model
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

    def _check_regime(self, observed_price_series):
        """
        Check current volatility regime by finding the most probable state of underlying Markov chain with Viterbi algorithm
        """
        current_regime = self.hmm_model.predict(observed_price_series)[-1]
        if current_regime = 0:
            return "low"
        else:
            return "high"

    def _buy_and_hold(backtest_period_daily_prices, portfolio):
        """
        Performs buy-and-hold investment strategy
        """
        for day in backtest_period_daily_prices:
            portfolio.append(day)

    def _regime_filter_strategy(backtest_period_daily_prices, portfolio):
        """
        Performs buy-and-hold strategy with HMM regime filter. If regime is 'low' – meaning low volatility – we go long or maintain
        our long position. If it's 'high' we sell or do nothing if already not invested.
        """
        DATE = 0
        PRICE = 1
        is_invested = True
        for idx, day in enumerate(backtest_period_daily_prices):
            # Start invested
            if day[DATE] == self.start_date:
                portfolio.append(day)
                continue
            else:
                current_portfolio_value = portfolio[-1][PRICE]
                # This is 1 in the beginning, but increases when portfolio outperforms and vice versa
                number_of_shares = day[PRICE] / current_portfolio_value
                previous_day = idx - 1
                current_regime = self._check_regime(backtest_period_daily_prices[:previous_day])
                if current_regime == "low":
                    # Calculate new value based on amount of shares
                    new_portfolio_value = day[PRICE] * number_of_shares
                    new_day = [day[DATE], new_portfolio_value]
                    portfolio.append(new_day)
                    is_invested = True
                elif current_regime == "high":
                    if is_invested:
                        # If invested, we sell. So new portfolio value is the same as previous day
                        new_day = [day[DATE], current_portfolio_value]
                        portfolio.append(new_day)
                        is_invested = False
                    else:
                        new_day = [day[DATE], current_portfolio_value]
                        portfolio.append(new_day)

    def run(self):
        """
        Run backtest
        """
        backtest_period_daily_prices = self._get_backtest_period(self.daily_prices, self.start_date, self.end_date)
        # Portfolio contains the date and current portfolio value
        portfolio = []
        # Check which strategy
        if self.strategy == "buy-and-hold":
            # Loop through all dates in backtest period
            _buy_and_hold(backtest_period_daily_prices, portfolio)
            return portfolio

        elif self.strategy == "regime-model":
            _regime_filter_strategy(backtest_period_daily_prices, portfolio)
            return portfolio
