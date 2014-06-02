"""
test_fft.py

Testing code for FFT, plotting, etc.

Author: Mahesh Venkitachalam
Website: electronut.in

"""

import numpy as np
import sys
from matplotlib import pyplot
from time import sleep
import argparse
import pyaudio

# get pyaudio input device
def getInputDevice(p):
    index = None
    nDevices = p.get_device_count()
    print('Found %d devices:' % nDevices)
    for i in range(nDevices):
        deviceInfo = p.get_device_info_by_index(i)
        print(deviceInfo)
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

# grab some audio data
def grabAudio(fileName):
    
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
    loop = True
    while loop:
        # read a chunk of data
        data  = stream.read(fftLen)
        f = open(fileName, 'wb')
        f.write(data)
        f.close()
        loop = False

def showAudioFFT(fileName):
    f = open(fileName, 'rb')
    y = f.read()
    f.close()
    x = range(2048)
    y = np.frombuffer(y, np.int16)
    pyplot.plot( x, y, '-' )
    pyplot.show()


# main() function
def main():
    # use sys.argv if needed
    print('testing FFT...')
    
    grabAudio('song.bin')
    showAudioFFT('song.bin')
  

# call main
if __name__ == '__main__':
    main()
