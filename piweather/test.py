import numpy as np
from matplotlib import pyplot


def decodeDH11Data(data):
    """
    decode DH11 data from string.
    """
    # store previous value
    prev = 0
    # store count to keep tack of oulse width
    count = 0
    # store decoded string here
    bits = ''
    # iterate through data
    for i in range(len(data)):
        # low to high transition
        if prev == 0 and data[i] == 1:
            # reset counter
            count = 1
        # high to low transition
        elif prev == 1 and data[i] == 0:
            # detect 1 vs 0
            if count > 3:
                bits += '1'
            else:
                bits += '0'
        # increment count
        else:
            count += 1
        # update prev value
        prev = data[i]

    #print len(bits)
    #print bits

    # convert string to integers
    data = []
    for i in range(0, 40, 8):
        data.append(int(bits[i:i+8], 2))
    # verify checksum
    if (sum(data[:4]) == data[4]):
        # print('checksum verified')
        # convert to float strings
        strRH = str(data[0]) + '.' + str(data[1])
        strT = str(data[2]) + '.' + str(data[3])
        return (strRH, strT)
    return None

f = open('samples.txt')
vals = [int(i) for i in f.read().split()]
f.close()
# convert
data = vals[1::2]

d = decodeDH11Data(data)
if d:
    print("RH = %s, T = %s" % (d[0], d[1]))

# plot
x = np.array(vals[::2])
y = np.array(vals[1::2])
pyplot.axis([-1, 1.01*np.max(x), 0, 1.5])
pyplot.plot(x, y, 'o-')

# show plot
pyplot.show()
