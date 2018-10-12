import numpy
from datetime import datetime

class DatastreamCsvPriceHandler(object):
    """
    Thomson-Reuters Datastream data reader. Handles daily stock market price data.
    """

    def __init__(self, csv_file):
        """
        Takes the csv_file.
        """
        self.csv_file = csv_file
        self.daily_prices = self._get_daily_prices(self)
        self.daily_returns = self._get_daily_returns(self.daily_prices)

    def _read_csv(self, csv_file):
        """
        Read CSV file.
        """
        with open(self.csv_file, "r") as price_data:
            price_series = {}
            is_price_series = False
            for line in price_data:
                fields = line.split(";")
                # Check for currency, price series starts after that
                if fields[0] == "CURRENCY":
                    is_price_series = True
                    continue
                # Start collecting price information
                if is_price_series:
                    date = fields[0]
                    # Strip newline from the end and convert comma to dot ie. '92,06\n' -> '92.06'
                    price = fields[1].strip().replace(",", ".")
                    price = float(price)
                    # Convert date to datetime object
                    date = datetime.strptime(date, "%d.%m.%Y")
                    # Collect dates and prices to dictionary
                    price_series[date] = price
        return price_series

    def _get_daily_prices(self, csv_file):
        """
        Return numpy array with shape = (days, 2) containing dates and prices
        """
        price_series = self._read_csv(self)
        daily_prices = numpy.array(list(price_series.items()))
        return daily_prices

    def _get_daily_returns(self, daily_prices):
        """
        Return daily percentage returns
        """
        DATE = 0
        PRICE = 1
        daily_returns = []
        # Can't compute for first day of price series, so start at second bar
        for idx in range(1, len(daily_prices)):
            # contains date and return
            one_day = []
            previous_day = daily_prices[idx-1]
            current_day = daily_prices[idx]
            # Calculates percentage return
            daily_return = (current_day[PRICE] - previous_day[PRICE])/previous_day[PRICE]
            one_day.append(current_day[DATE])
            one_day.append(daily_return)
            daily_returns.append(one_day)
        return numpy.array(daily_returns)
