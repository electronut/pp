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

# save spiros to image
def saveDrawing():
    # generate unique file name
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro-' + dateStr 
    print('saving drawing to %s.eps/png' % fileName)
    # get tkinter canvas
    canvas = turtle.getcanvas()
    # save postscipt image
    canvas.postscript(file = fileName + '.eps')
    # use PIL to convert to PNG
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')


# main() function
def main():
  # use sys.argv if needed
  print('generating spirograph...')
  # create parser
  parser = argparse.ArgumentParser(description="Spirograph...")
  
  # add expected arguments
  parser.add_argument('--sparams', nargs=3, dest='sparams', required=False)

  # parse args
  args = parser.parse_args()
  
  # set title
  turtle.title("Spirographs!")
  # add key handler for saving images
  turtle.onkey(saveDrawing, "s")
  # start listening 
  turtle.listen()

  if args.sparams:
      # draw spirograph with given parameters
      drawSprio()
  else:
      drawRandomSpiros()

  drawSpiroTurtle(0, 0)

  # start turtle main loop
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

- home work

- spiral
- pause drawing
- align turtle
"""
