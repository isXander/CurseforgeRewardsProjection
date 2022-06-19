import numpy as np
from currency_converter import CurrencyConverter
import matplotlib.pyplot as graph
import locale
import os


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


try:
    terminal_width = os.get_terminal_size().columns
except OSError:
    terminal_width = 70

print("-" * terminal_width)
print("Curseforge Rewards Projector by isXander")
print("https://github.com/isXander/CurseforgeRewardsProjection")
print("This script can obviously not see into the future and all numbers given are an estimate based on the data "
      "given. The more data, the more accurate of an estimate.")
print("-" * terminal_width)
print()

show_graphs = input("Display graphs [y/n]: ").lower() in ['true', 'y', '1', 'yes']

input('Press enter when "./points_earned.txt" is present with the format of\n1.25\n3.54\netc..\n')

file = open("./points_earned.txt", "r")
data = np.array(list(map(float, file.readlines())))
file.close()

if data[0] > data[-1]:
    data = data[::-1]

if show_graphs:
    graph.figure(1)
    graph.plot(indices(data), data)
    graph.title("Points Graph")
    graph.xlabel("Day")
    graph.ylabel("Points Earned")
    graph.show()

diff = reject_outliers(np.diff(data))
diff_indices = indices(diff)
coefficient_x2, coefficient_x, y_intercept = np.polyfit(diff_indices, diff, 2)

if show_graphs:
    graph.figure(2)
    graph.plot(diff_indices, diff)
    graph.plot(diff_indices, coefficient_x2 * diff_indices ** 2 + coefficient_x * diff_indices + y_intercept)
    graph.title("Points Difference Graph")
    graph.xlabel("Day")
    graph.ylabel("Difference")
    graph.show()

days = int(input("Days to calculate: "))
if days / len(diff) > 1.:
    print("Warning: too little data to provide a realistic estimate")
existing_balance = int(input("Existing points balance: "))

starting = data[-1]

amount = existing_balance
for i in range(days):
    x = len(diff) + i
    point_increase = coefficient_x2 * x ** 2 + coefficient_x * x + y_intercept
    amount += starting + point_increase * i

point_value = 0.05
usd = amount * point_value

locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
currency = locale.localeconv()['int_curr_symbol'].strip()
symbol = locale.localeconv()['currency_symbol']
converter = CurrencyConverter()
converted_currency = "~" + symbol + np.format_float_positional(
    converter.convert(usd, "USD", currency),
    precision=2, fractional=True, min_digits=2
)
usd_formatted = "$" + np.format_float_positional(usd, precision=2, fractional=True, min_digits=2)

print("In", days, "days you will have made", converted_currency,
      "(" + usd_formatted + " / " + str(int(amount)) + " points)")
