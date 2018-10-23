import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.colors
import pandas as pandas

random = pandas.read_csv('/Users/apple/Desktop/1K-symulation/random.csv')

print


fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)

ax.plot([1, 2, 3, 4, 10], [10, 20, 25, 30, 100], color='lightblue', linewidth=3)
ax.scatter([0.3, 3.8, 1.2, 2.5], [11, 25, 9, 26], color='darkgreen', marker='^')


# ax.set_yscale('log')
ax.tick_params(axis='both', which='major', labelsize=10)
# ax.set_xlim(0, 150)

ax.legend(['MAX', 'RANDOM', 'GREEDY'])

plt.show()
#
fig.savefig("1GREEDYx1RANDOMx1MAX_the_same_net.png", dpi = (200))