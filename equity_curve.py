import matplotlib.pyplot as plt
import re
import seaborn

portfolio_value = []
with open("../OMXH25_regime.txt", "r") as omxh:
    for line in omxh:
        line =  re.sub("[\[\]lowhigh\n'']", '', line)
        portfolio_value.append(float(line))
plt.plot(portfolio_value)
plt.show()
