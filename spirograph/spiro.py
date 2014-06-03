"""
spiro.py

A python program that simulates a Sprirograph.

Author: Mahesh Venkitachalam
Website: electronut.in
"""

import sys, random, argparse
import numpy as np
import math
import turtle
import random

# draw circle using turtle
def drawCircleTurtle(x, y, r):
    # got to start of circle
    turtle.up()
    turtle.setpos(x + r, y)
    turtle.down()


    # draw circle
    for i in range(0, 365, 5):
        a = math.radians(i)
        turtle.setpos(x + r*math.cos(a), y + r*math.sin(a))
    
# draw spirograph using Turtle
def drawSpiroTurtle(xc, yc):
    # parameters
    R = 100
    r = random.randint(0, 60)
    k = r/R
    l = random.random()

    # set color
    turtle.color(random.random(),
                 random.random(),
                 random.random())

    print(R, r, l)
    # got to start
    turtle.up()
    # draw spirograph
    for i in range(0, 3600, 2):
        a = math.radians(i)
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        if i == 2:
            turtle.down()
        turtle.setpos(xc + x, yc + y)
    

# main() function
def main():
  # use sys.argv if needed
  print('generating spirograph...')
  # create parser
  parser = argparse.ArgumentParser(description="Sprirograph...")
  """
  # add expected arguments
  parser.add_argument('--file', dest='imgFile', required=True)
  parser.add_argument('--scale', dest='scale', required=False)
  parser.add_argument('--out', dest='outFile', required=False)
  parser.add_argument('--cols', dest='cols', required=False)
  parser.add_argument('--morelevels',dest='moreLevels',action='store_true')
  """

  # parse args
  # args = parser.parse_args()
  #drawCircleTurtle(10, 10, 50)

  drawSpiroTurtle(100, 100)
  
  input('press enter to exit')

# call main
if __name__ == '__main__':
  main()
