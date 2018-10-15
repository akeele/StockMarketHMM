from run_backtest import Backtest
from data_reader import DatastreamCsvPriceHandler
from train_hmm import RegimeHmmModel
import pickle
from datetime import datetime
import argparse

def get_training_data(daily_returns, start_date, end_date):
    """
    Return training data
    """
    DATE = 0
    start = 0
    end = 0
    for idx, day in enumerate(daily_returns):
        # Check for starting date
        if day[DATE] == start_date:
            start = idx
        elif day[DATE] == end_date:
            end = idx
            break

    return daily_returns[start:end]

if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="Run backtests on stock market")
    argparser.add_argument("--csv-file", default=None, help="CSV file containing stock index prices or individual stock prices")
    argparser.add_argument("--backtest-start", default=None, help="Start date of backtest. Give like this 'day.month.year'")
    argparser.add_argument("--backtest-end", default="31.12.2017", help="End date of backtest")
    argparser.add_argument("--training-start", default=None, help="Start date of training period")
    argparser.add_argument("--training-end", default=None, help="End date of training period")
    argparser.add_argument("--pickle-path", default=None, help="File to store trained HMM")


    args = argparser.parse_args()

    # Get daily prices and returns, as numpy arrays with shape (days, 2). First column is dates, second prices or percentage returns.
    price_handler = DatastreamCsvPriceHandler(args._csv_file)
    daily_prices = price_handler.daily_prices
    daily_returns = price_handler.daily_returns

    # Train HMM
    start_date = datetime.strptime(args._training_start, '%d.%m.%Y')
    end_date = datetime.strptime(args._training_end, '%d.%m.%Y')
    training_data = get_training_data(daily_returns, start_date, end_date)
    RegimeHmmModel(training_data, n_states=2, n_iters=1000, pickle_path=args._pickle_path)

    # Run backtest
    
