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
from PIL import Image
from datetime import datetime    

# save drawing as image
# put params in EXIF data
def saveImage(fileName):
    pass

# draw spirograph using Turtle
def drawSpiroTurtle(xc, yc):
    # parameters
    R = 200
    r = random.randint(0, 90)
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
    theta = 360*10
    for i in range(0, theta, 2):
        a = math.radians(i)
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        if i == 2:
            turtle.down()
        turtle.setpos(xc + x, yc + y)
    
# class that creates a Spirograph
class Spiro:
    def __init__(self, R, r, l, xc, yc):
        pass

def pauseDrawing():
    print('pause drawing')

def saveDrawing():
    print('saving drawing')

    # generate unique file name
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro-' + dateStr 

    canvas = turtle.getcanvas()
    canvas.postscript(file = fileName + '.eps')
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')

# main() function
def main():
  # use sys.argv if needed
  print('generating spirograph...')
  # create parser
  parser = argparse.ArgumentParser(description="Spirograph...")
  """
  # add expected arguments
  parser.add_argument('--file', dest='imgFile', required=True)
  parser.add_argument('--scale', dest='scale', required=False)
  parser.add_argument('--out', dest='outFile', required=False)
  parser.add_argument('--cols', dest='cols', required=False)
  parser.add_argument('--morelevels',dest='moreLevels',action='store_true')
  """

  parser.add_argument('--sparams', nargs=3, dest='sparams', required=True)

  # parse args
  args = parser.parse_args()

  print(args)

  #drawCircleTurtle(10, 10, 50)

  turtle.title("Spirographs!")

  turtle.onkey(pauseDrawing, "a")

  turtle.onkey(saveDrawing, "s")

  turtle.listen()

  drawSpiroTurtle(0, 0)

  turtle.mainloop()

# call main
if __name__ == '__main__':
  main()

"""
- keyboard - pause
- keyboard - save file - time stamp, EXIF
- multiple random spiros
- manual spiro params
- peroidicity

"""
