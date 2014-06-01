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
    print('Found %d devices:' % nDevices)
    for i in range(nDevices):
        deviceInfo = p.get_device_info_by_index(i)
        devName = deviceInfo['name']
        print(devName)
        # look for the "input" keyword
        # choose the first such device as input
        # change this loop to modify this behavior
        # maybe you want "mic"?
        if not index:
            if 'input' in devName.lower():
                index = i
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
          fftVals = numpy.fft.rfft(dataArray)//fftLen
          # get absolute values
          fftVals = numpy.abs(fftVals)
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
