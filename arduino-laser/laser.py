"""

laser.py

Description: Analyze audio input using FFT and send motor speed/direction 
              information via serial port. This is used to create 
              Lissajous-like figures using 2 motors with mirrors, 
              a laser pointer, and an Arduino microcontroller.

Author: Mahesh Venkitachalam
Website: electronut.in

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
            strIn = raw_input()
            vals = [int(val) for val in strIn.split()[:4]]
            vals.insert(0, ord('H'))
            data = struct.pack('BBBBB', *vals)
            ser.write(data)
    except:
        print('exiting...')
        # shut off motors
        vals = [ord('H'), 0, 1, 0, 1]
        data = struct.pack('BBBBB', *vals)
        ser.write(data)
        ser.close()

# automatic test for sending motor speeds
def autoTest(ser):
    print('staring automatic test...')
    try:
        while True:
            # for each direction combination
            for dr in [(0, 0), (1, 0), (0, 1), (1, 1)]:
                # for a range of speeds
                for j in range(25, 180, 10):
                    for i in range(25, 180, 10):
                        vals = [ord('H'), i, dr[0], j, dr[1]]
                        print(vals[1:])
                        data = struct.pack('BBBBB', *vals)
                        ser.write(data)
                        sleep(0.1)
    except KeyboardInterrupt:
        print('exiting...')
        # shut off motors
        vals = [ord('H'), 0, 1, 0, 1]
        data = struct.pack('BBBBB', *vals)
        ser.write(data)
        ser.close()


# get pyaudio input device
def getInputDevice(p):
    index = None
    nDevices = p.get_device_count()
    print('Found %d devices. Select input device:' % nDevices)
    # print all devices found
    for i in range(nDevices):
        deviceInfo = p.get_device_info_by_index(i)
        devName = deviceInfo['name']
        print("%d: %s" % (i, devName))
    # get user selection
    try:
        # get user selection and convert to integer
        index = int(input())
    except:
        pass

    # print out chosen device
    if index is not None:
        devName = p.get_device_info_by_index(index)["name"]
        print("Input device chosen: %s" % devName)
    return index

# fft of live audio
def fftLive(ser):
  # initialize pyaudio
  p = pyaudio.PyAudio()

  # get pyAudio input device index
  inputIndex = getInputDevice(p)

  # set FFT sample length
  fftLen = 2**11
  # set sample rate
  sampleRate = 44100

  print('opening stream...')
  stream = p.open(format = pyaudio.paInt16,
                  channels = 1,
                  rate = sampleRate,
                  input = True,
                  frames_per_buffer = fftLen,
                  input_device_index = inputIndex)
  try:
      while True:
          # read a chunk of data
          data  = stream.read(fftLen)
          # convert to numpy array
          dataArray = numpy.frombuffer(data, dtype=numpy.int16)

          # get FFT of data
          fftVals = numpy.fft.rfft(dataArray)*2.0/fftLen
          # get absolute values of complex numbers
          fftVals = numpy.abs(fftVals)
          # get average of 3 frequency bands
          # 0-100 Hz, 100-1000 Hz and 1000-2500 Hz
          levels = [numpy.sum(fftVals[0:100])/100,
                    numpy.sum(fftVals[100:1000])/900,
                    numpy.sum(fftVals[1000:2500])/1500]


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
          vals[1] = int(5*levels[0]) % 255
          # speed2
          vals[3] = int(100 + levels[1]) % 255

          # dir
          d1 = 0
          if levels[2] > 0.1:
              d1 = 1
          vals[2] = d1
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
    parser.add_argument('--mtest', action='store_true', default=False)
    parser.add_argument('--atest', action='store_true', default=False)
    args = parser.parse_args()

    # open serial port
    strPort = args.serial_port_name
    print('opening ', strPort)
    ser = serial.Serial(strPort, 9600)
    if args.mtest:
        manualTest(ser)
    elif args.atest:
        autoTest(ser)
    else:
        fftLive(ser)
        
# call main function
if __name__ == '__main__':
    main()
