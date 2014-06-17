import numpy as np
from matplotlib import pyplot

f = open('samples.txt')
vals = [int(i) for i in f.read().split()]
f.close()

x = np.array(vals[::2])
y = np.array(vals[1::2])
pyplot.axis([-1, 1.01*np.max(x), 0, 1.5])
pyplot.plot(x, y, '-')

# show plot
pyplot.show()
