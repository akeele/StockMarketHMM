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
                    price = fields[1].strip()
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
