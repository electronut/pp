"""

laser.py

Author: Mahesh Venkitachalam

Description: Analyze audio input using FFT and send motor speed/direction 
              information via serial port. This is used to create Lissajous 
              figures using 2 motors with mirrors, a laser pointer, and 
              an Arduino microcontroller.

Sample Run: 

$python laser.py --port /dev/tty.usbserial-A7006Yqb
opening  /dev/tty.usbserial-A7006Yqb
opening stream...
^Cstopping...
cleaning up
"""

import sys, serial, struct
import pyaudio
import numpy
import math
from time import sleep
import argparse

# manual test for sending motor speeds
def manualTest(ser):
    print('staring manual test...')
    try:
        while True:
            print('enter motor control info: eg. < 100 1 120 0 >')
            strIn = input()
            vals = [int(val) for val in strIn.split()[:4]]
            vals.insert(0, ord('H'))
            data = struct.pack('BBBBB', *vals)
            ser.write(data)
    except KeyboardInterrupt:
        print('exiting...')
        # shut off motors
        vals = [ord('H'), 0, 1, 0, 1]
        data = struct.pack('BBBBB', *vals)
        ser.write(data)
        ser.close()

# fft of live audio
def fftLive(ser):
  p = pyaudio.PyAudio()
  fftLen = 2**11
  sampleRate = 44100

  # get input device index:
  # If this part of the code fails, please try the following 
  # inside the Python interpreter
  #
  # >>> import pyaudio
  # >>> p = pyaudio.PyAudio()
  # >>> n = p.get_device_count()
  # >>> p.get_device_info_by_index(i) for i in range(n)]
  # now look through this list, and replace the line below
  # with the index of the device named 'input' or 'mic'
  id_index = p.get_default_input_device_info()['index']

  print('opening stream...')
  stream = p.open(format = pyaudio.paInt16,
                  channels = 1,
                  rate = sampleRate,
                  input = True,
                  frames_per_buffer = fftLen,
                  input_device_index = id_index)
  try:
      while True:
          # read a chunk of data
          data  = stream.read(fftLen)
          # convert to numpy array
          dataArray = numpy.frombuffer(data, dtype=numpy.int16)
          n = len(dataArray)
          # get FFT of data
          fftVals = numpy.fft.fft(dataArray)/n
          # get absolute values
          fftVals = numpy.abs(fftVals[list(range(int(n/2)))])
          sz = len(fftVals)
          # average frequency information in nl bins
          nl = 16
          levels = [sum(fftVals[i:i+int(sz/nl)])/(int(sz/nl)) for i in range(0, sz, int(sz/nl))]
          # Apply scale
          # This is tricky, because we have only a fragment of the 
          # audio, and we can't normalize it properly. 
          # So this is a bit of a hack to get it in the [0-255] value
          # range, which is the motor speed
          levels = [int(255*l/10.0) % 255  for l in levels]
          
          # The data sent is of the form:
          # 'H' (header), speed1, dir1, speed2, dir2
          vals = [ord('H'), 100, 1, 100, 1]

          # The code below sets speed/direction based on information 
          # in the frequency bin. This is totally arbitary - depends 
          # on the effect you are trying to create. The goal is to 
          # generate 4 values (s1 [0-255], d1[0/1], s2[0-255], d2[0/1])
          # from the constantly changing frequency content, so the motors 
          # are in sync with the music.

          # speed1
          vals[1] = levels[0]
          # dir1
          d1 = 0
          if levels[1] > 128:
              d1 = 1
          vals[2] = d1
          # speed2
          vals[3] = (50 + levels[2]) % 255
          # dir2
          vals[4] = 0
          # pack data
          data = struct.pack('BBBBB', *vals)
          # write data to serial port
          ser.write(data)
          # a slight pause
          sleep(0.001)
  except KeyboardInterrupt:
      print('stopping...')
  finally:
      print('cleaning up')
      stream.close()
      p.terminate()
      # shut off motors
      vals = [ord('H'), 0, 1, 0, 1]
      data = struct.pack('BBBBB', *vals)
      ser.write(data)
      # close serial
      ser.flush()
      ser.close()

# main method
def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='Analyzes audio input and sends motor control information via serial port')
    # add arguments
    parser.add_argument('--port', dest='serial_port_name', required=True)
    parser.add_argument('--test', action='store_true', default=False)
    args = parser.parse_args()

    # open serial port
    strPort = args.serial_port_name
    print('opening ', strPort)
    ser = serial.Serial(strPort, 9600)
    if args.test:
        manualTest(ser)
    else:
        fftLive(ser)
        
# call main function
if __name__ == '__main__':
    main()
