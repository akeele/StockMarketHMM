import matplotlib.pyplot as plt
import re
#import seaborn
import sys
import numpy
import datetime

first_portfolio_file = sys.argv[1] # Buy-and-hold
second_portfolio_file = sys.argv[2] # Regime-filter

def get_portfolio_values_list(portfolio_file):
    portfolio_value = []
    with open(portfolio_file, "r") as omxh:
        for line in omxh:
            line =  re.sub("[lowhigh\n]", '', line)
            line = line.split(" ")
            line[1] = float(line[1])
            portfolio_value.append(line)
    return portfolio_value

first_portfolio_value = get_portfolio_values_list(first_portfolio_file)
second_portfolio_value = get_portfolio_values_list(second_portfolio_file)


plt.style.use("ggplot")
dates = [item[0] for item in first_portfolio_value]
equity_first = [item[1] for item in first_portfolio_value]
equity_second = [item[1] for item in second_portfolio_value]
dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates]
plt.plot(dates, equity_first)
plt.plot(dates, equity_second)
plt.legend(["Buy-and-hold", "Regime-filter"], loc='upper left')
plt.show()
