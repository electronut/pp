"""
piweather.py

Add description here.

Author: Mahesh Venkitachalam
"""

import sys
import wiringpi2 as wiringpi
from time import sleep  

# main() function
def main():
    # use sys.argv if needed
    print 'hello'
    wiringpi.wiringPiSetupPhys() 
    wiringpi.pinMode(18, 1)
    while True:  
        wiringpi.digitalWrite(18, 1)  # Turn on light
        sleep(2)  
        wiringpi.digitalWrite(18, 0)  # Turn on light
        sleep(2)


# call main
if __name__ == '__main__':
    main()
