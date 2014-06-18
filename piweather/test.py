import numpy as np
from matplotlib import pyplot

def getDHT11Data(pinNum):
    """
    Get data from DHT11 conencted to pinNum (board)
    """
    
    # set pin as output
    wiringpi.wiringPiSetupPhys() 
    wiringpi.pinMode(pinNum, 1)

    # pull down for 20 ms = 20000 us
    wiringpi.digitalWrite(pinNum, 0) 
    wiringpi.delayMicroseconds(20000)
    # pull up
    wiringpi.digitalWrite(pinNum, 1) 

    # set pin as input
    wiringpi.pinMode(pinNum, 0)
    # wait for 20us
    wiringpi.delayMicroseconds(18)

    # read data for t = (50 + 70) * 40 + 160 us
    # ~ 5 ms = 5000 us    
    srate = 10
    N = 5000//srate
    samples = numpy.zeros(N, numpy.int16)
    for i in range(N):
        # read pin
        val = wiringpi.digitalRead(pinNum)
        samples[i] = val
        # sample every 20 microseconds
        #wiringpi.delayMicroseconds(1)    

    return samples

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

    print len(bits)
    print bits

    if len(bits) == 40:
        # convert string to integers
        x = []
        for i in range(0, 40, 8):
            x.append(int(bits[i:i+8], 2))
        # verify checksum
        if (sum(x[:4]) == x[4]):
            # print('checksum verified')
            # convert to float strings
            strRH = str(x[0]) + '.' + str(x[1])
            strT = str(x[2]) + '.' + str(x[3])
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
