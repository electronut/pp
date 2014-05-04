"""
ldr.py

Display analog data from Arduino using Python (matplotlib)

Author: Mahesh Venkitachalam
Website: electronut.in
"""

import serial, argparse
from collections import deque

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen):
      # open serial port
      self.ser = serial.Serial(strPort, 9600)

      self.a0Vals = deque([0.0]*maxLen)
      self.a1Vals = deque([0.0]*maxLen)
      self.maxLen = maxLen

  # add data
  def add(self, data):
      assert(len(data) == 2)
      self.addToDeq(self.a0Vals, data[0])
      self.addToDeq(self.a1Vals, data[1])

  # add to deque, pop oldest value
  def addToDeq(self, buf, val):
      buf.pop()
      buf.appendleft(val)

  # update plot
  def update(self, frameNum, a0, a1):
      try:
          line = self.ser.readline()
          data = [float(val) for val in line.split()]
          # print data
          if(len(data) == 2):
              self.add(data)
              a0.set_data(range(self.maxLen), self.a0Vals)
              a1.set_data(range(self.maxLen), self.a1Vals)
      except:
          pass

      return a0, a1

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
  parser.add_argument('--N', dest='maxLen', required=False)

  # parse args
  args = parser.parse_args()
  
  #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort = args.port

  print('reading from serial port %s...' % strPort)

  # plot parameters
  maxLen = 100
  if args.maxLen:
      maxLen = int(args.maxLen)

  # create plot object
  analogPlot = AnalogPlot(strPort, maxLen)

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, maxLen), ylim=(0, 1023))
  a0, = ax.plot([], [])
  a1, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(a0, a1), 
                                 interval=20)

  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
