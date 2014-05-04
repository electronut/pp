"""
ldr.py

Display analog data from Arduino using Python (matplotlib)

Author: Mahesh Venkitachalam
Website: electronut.in
"""

import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen):
      # open serial port
      self.ser = serial.Serial(strPort, 9600)

      self.ax = deque([0.0]*maxLen)
      self.ay = deque([0.0]*maxLen)
      self.maxLen = maxLen

      # set plot to animated
      plt.ion() 
      self.axline, = plt.plot(self.ax)
      self.ayline, = plt.plot(self.ay)
      plt.ylim([0, 1023])

  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)

  # add data
  def add(self, data):
      assert(len(data) == 2)
      self.addToBuf(self.ax, data[0])
      self.addToBuf(self.ay, data[1])

  # update plot
  def update(self):
      self.axline.set_ydata(self.ax)
      self.ayline.set_ydata(self.ay)
      plt.draw()

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    

# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)

  # parse args
  args = parser.parse_args()
  
  #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort = args.port

  print('reading from serial port %s...' % strPort)

  # plot parameters
  analogPlot = AnalogPlot(strPort, 100)

  print('plotting data...')

  ser = analogPlot.ser
  while True:
    try:
      line = ser.readline()
      data = [float(val) for val in line.split()]
      #print data
      if(len(data) == 2):
        analogPlot.add(data)
        analogPlot.update()
    except KeyboardInterrupt:
      print('exiting')
      break
  
  # clean up
  analogPlot.close()

# call main
if __name__ == '__main__':
  main()
