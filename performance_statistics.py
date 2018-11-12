import sys
import re
import numpy


portfolio_file = sys.argv[1]

regimes = []
with open(portfolio_file, "r") as p:
    for line in p:
        line = re.sub("[0-9\n\.\-]", '', line)
        line = line.strip()
        regimes.append(line)
        
print("Days:", len(regimes))
number_of_lows = 0
number_of_highs = 0
for day in regimes:
    if day == "low":
        number_of_lows += 1
    elif day == "high":
        number_of_highs += 1

print("Number of low regimes:", number_of_lows)
print("Number of high regimes:", number_of_highs)
        
portfolio_value = []
with open(portfolio_file, "r") as portfolio:
    for line in portfolio:
        line = re.sub("[highlow\n]", '', line)
        line = line.split(" ")
        portfolio_value.append(float(line[1]))


portfolio_returns = []
for idx, price in enumerate(portfolio_value):
    if idx == 0:
        continue
    daily_return = (price - portfolio_value[idx-1]) / portfolio_value[idx-1]
    portfolio_returns.append(daily_return)

portfolio_returns = numpy.asarray(portfolio_returns)

annualized_sharpe = numpy.sqrt(252) *  (numpy.mean(portfolio_returns)) / numpy.std(portfolio_returns)
print("Annualized Sharpe ratio:", annualized_sharpe)

annualized_sortino = numpy.sqrt(252) *  (numpy.mean(portfolio_returns)) / numpy.std(portfolio_returns[portfolio_returns < 0])
print("Annualized Sortino ratio:", annualized_sortino)

portfolio_equity = numpy.asarray(portfolio_value)

def calculate_max_drawdown(equity):
    """ Get max drawdown """
    high_watermark = numpy.zeros(len(equity))
    for time in range(len(equity)):
        if time == 0:
            high_watermark[time] = equity[time]
        else:
            high_watermark[time] = max(high_watermark[time-1], equity[time])

    drawdowns = (high_watermark - equity) / high_watermark
    return numpy.max(drawdowns)

print("Max drawdown:", calculate_max_drawdown(portfolio_equity))

