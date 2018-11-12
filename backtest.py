import numpy

class Backtest(object):
    """
    Create backtest
    """

    def __init__(self, daily_prices, daily_returns, strategy, start_date, end_date, high_regime, hmm_model):
        """
        Takes strategy, which defines the strategy, start date and end date of backtest
        """
        self.daily_prices = daily_prices
        self.daily_returns = daily_returns
        self.strategy = strategy
        self.hmm_model = hmm_model
        self.start_date = start_date
        self.end_date = end_date
        self.high_regime = high_regime

    def _get_index_before_backtest(self, daily_returns):
        """
        Returns index of date just before backtest start date
        """
        DATE = 0
        end = 0
        for idx, day in enumerate(daily_returns):
            if day[DATE] == self.start_date:
                end = idx

        return end

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

    def _check_regime(self, observed_return_series, high_regime):
        """
        Check current volatility regime by finding the most probable state of underlying Markov chain with Viterbi algorithm
        """
        observed_return_series = numpy.column_stack([observed_return_series[:,1]])
        current_regime = self.hmm_model.predict(observed_return_series)[-1]
        if current_regime == high_regime:
            return "high"
        else:
            return "low"

    def _buy_and_hold(self, backtest_period_daily_prices, portfolio):
        """
        Performs buy-and-hold investment strategy
        """
        DATE = 0
        VALUE = 1
        portfolio_value = 100
        portfolio_information = []
        backtest_start_date_index = self._get_index_before_backtest(self.daily_returns)
        for idx, day in enumerate(backtest_period_daily_prices):
            days_return = self.daily_returns[:(backtest_start_date_index + idx + 1)][-1]
            portfolio_value = portfolio_value * (1 + days_return[VALUE])
            portfolio_information = [day[DATE], portfolio_value]
            portfolio.append(portfolio_information)


    def _regime_filter_strategy(self, daily_prices, portfolio):
        """ Regime filter strategy with portfolio value calculated with returns """
        DATE = 0
        VALUE = 1
        REGIME = 2
        portfolio_value = 100
        portfolio_information = []
        backtest_start_date_index = self._get_index_before_backtest(self.daily_returns)
        # Loop through backtest days
        for idx, day in enumerate(daily_prices):
            # Check yesterdays volatility regime
            observed_return_series = self.daily_returns[:(backtest_start_date_index + idx)]
            current_regime = self._check_regime(observed_return_series, self.high_regime)
            # Check that day matches
            current_day_return = self.daily_returns[:(backtest_start_date_index + idx + 1)][-1]
            if current_day_return[DATE] != day[DATE]:
                print("Should be the same day!")
                print(current_day_return[DATE])
                print(day[DATE])
                break
            # Start invested
            if idx == 0:
                portfolio_information = [day[DATE], portfolio_value, current_regime]
                portfolio.append(portfolio_information)
            else:
                # If regime is low volatility regime
                if current_regime == "low":
                    # Calculate new portfolio value by multiplying with day's return
                    portfolio_value = portfolio_value * (1 + current_day_return[VALUE])
                    portfolio_information = [day[DATE], portfolio_value, current_regime]
                    portfolio.append(portfolio_information)
                # If regime is high volatility regime
                elif current_regime == "high":
                    if portfolio[-1][REGIME] == "low":
                        # Sell all assets
                        portfolio_value = portfolio_value * (1 + current_day_return[VALUE])
                        portfolio_information = [day[DATE], portfolio_value, current_regime]
                        portfolio.append(portfolio_information)
                    else:
                        # Stay in cash
                        portfolio_information = [day[DATE], portfolio_value, current_regime]
                        portfolio.append(portfolio_information)


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
            self._buy_and_hold(backtest_period_daily_prices, portfolio)
            return portfolio

        elif self.strategy == "regime-filter":
            self._regime_filter_strategy(backtest_period_daily_prices, portfolio)
            return portfolio
