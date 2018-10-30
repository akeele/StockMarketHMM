import sys
import re
import numpy


portfolio_file = sys.argv[1]
portfolio_value = []
with open(portfolio_file, "r") as portfolio:
    for line in portfolio:
        line = re.sub("[\[\]highlow']", '', line)
        portfolio_value.append(float(line))


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
