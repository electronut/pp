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
    
    f = open('samples.txt', 'w')
    for i in range(len(samples)):
        f.write("%d %d\n" % (i, samples[i]))
    f.close()
    print('done')

# main() function
def main():
    # use sys.argv if needed
    print 'starting piweather...'
    
    getDHT11Data(16)

# call main
if __name__ == '__main__':
    main()
