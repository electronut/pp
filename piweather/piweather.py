"""
piweather.py

Add description here.

Author: Mahesh Venkitachalam
"""

import sys
import wiringpi2 as wiringpi
from time import sleep  

def blink():
    """
    Make LED connected to pin 18 (board) blink
    """
    wiringpi.wiringPiSetupPhys() 
    wiringpi.pinMode(18, 1)
    while True:  
        wiringpi.digitalWrite(18, 1)  # Turn on light
        sleep(2)  
        wiringpi.digitalWrite(18, 0)  # Turn on light
        sleep(2)


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
    wiringpi.delayMicroseconds(20)
    
    # read data for t = (50 + 70) * 40 + 160 us
    # ~ 5 ms = 5000 us    
    samples = []
    srate = 10
    N = 5000//srate
    for i in range(N):
        # read pin
        val = wiringpi.digitalRead(pinNum)
        samples.append(val)
        # sample every 20 microseconds
        #wiringpi.delayMicroseconds(srate)    
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

# main() function
def main():
    # use sys.argv if needed
    print 'starting piweather...'
    
    """
    f = open('samples.txt', 'w')
    for i in range(len(samples)):
        f.write("%d %d\n" % (i, samples[i]))
    f.close()
    print('done')
    """
    while True:
        data = getDHT11Data(16)
        d = decodeDH11Data(data)
        if d:
            print("RH = %s, T = %s" % (d[0], d[1]))
        sleep(2)
# call main
if __name__ == '__main__':
    main()
