import numpy as np
from currency_converter import CurrencyConverter
import matplotlib.pyplot as graph
import locale


def indices(data):
    arr = []
    for idx, _ in enumerate(data):
        arr.append(idx)
    return np.array(arr)


def reject_outliers(data, m=2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    return data[s < m]


input('Press enter when "./points_earned.txt" is present with the format of\n1.25\n3.54\netc..\n')

file = open("./points_earned.txt", "r")
data = np.array(list(map(float, file.readlines())))
file.close()

if data[0] > data[-1]:
    data = data[::-1]

graph.figure(1)
graph.plot(indices(data), data)
graph.title("Points Graph")
graph.xlabel("Day")
graph.ylabel("Points Earned")
graph.show()

diff = reject_outliers(np.diff(data))
diff_indices = indices(diff)
gradient, y_intercept = np.polyfit(diff_indices, diff, 1)
graph.figure(2)
graph.plot(diff_indices, diff)
graph.plot(diff_indices, gradient * diff_indices + y_intercept)
graph.title("Points Difference Graph")
graph.xlabel("Day")
graph.ylabel("Difference")
graph.show()

days = int(input("Days to calculate: "))
existing_balance = int(input("Existing points balance: "))

starting = data[-1]

amount = existing_balance
for i in range(days):
    point_increase = gradient * (len(diff) + i) + y_intercept
    amount += starting + point_increase * i

point_value = 0.05
usd = amount * point_value

locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
currency = locale.localeconv()['int_curr_symbol'].strip()
symbol = locale.localeconv()['currency_symbol']
converter = CurrencyConverter()
converted_currency = symbol + np.format_float_positional(
    converter.convert(usd, "USD", currency),
    precision=2, fractional=True, min_digits=2
)
usd_formatted = "$" + np.format_float_positional(usd, precision=2, fractional=True, min_digits=2)

print("In", days, "days you will have made", converted_currency, "(" + usd_formatted + " / " + str(int(amount)) + " points)")
