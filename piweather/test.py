import numpy as np
from matplotlib import pyplot

f = open('samples.txt')
vals = [int(i) for i in f.read().split()]
f.close()

# convert
data = vals[1::2]
prev = 0
count = 0
bits = ''
for i in range(len(data)):
    # low to high transition
    if prev == 0 and data[i] == 1:
        count = 1
    # high to low transition
    elif prev == 1 and data[i] == 0:
        if count > 3:
            bits += '1'
        else:
            bits += '0'
    # count
    else:
        count += 1
    prev = data[i]

print len(bits)
print bits

# plot
x = np.array(vals[::2])
y = np.array(vals[1::2])
pyplot.axis([-1, 1.01*np.max(x), 0, 1.5])
pyplot.plot(x, y, 'o-')

# show plot
pyplot.show()
