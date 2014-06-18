"""
piweather.py

A Web based Temperature/Humidity monitor using Raspberry Pi and DHT11.

Author: Mahesh Venkitachalam
"""

import sys
import RPi.GPIO as GPIO
from time import sleep  
import Adafruit_DHT

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT22, or Adafruit_AM2302.
sensor = Adafruit_DHT.DHT11

# Example using a Raspberry Pi with DHT sensor
# connected to pin 23.
pin = 23

def blink():
    """
    Make LED connected to pin 18 (board) blink
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.OUT)
    
    while True:
        try:
            GPIO.output(18, True)
            time.sleep(0.5)
            GPIO.output(18, False)
            time.sleep(0.5)
        except:
            print 'exiting...'
            # off
            GPIO.output(18, False)
            break

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

    pinNum = 16
    while True:

        # Try to grab a sensor reading.  
        # Use the read_retry method which will retry up
        # to 15 times to get a sensor reading 
        # (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).  
        # If this happens try again!
        if humidity is not None and temperature is not None:
            print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        else:
            print 'Failed to get reading. Try again!'

        """
        data = getDHT11Data(pinNum)
        d = decodeDH11Data(data)
        if d:
            print("RH = %s, T = %s" % (d[0], d[1]))
        """

        sleep(2)

# call main
if __name__ == '__main__':
    main()
