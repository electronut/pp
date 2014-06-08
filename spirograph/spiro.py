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


# draw spirograph
def drawSpiro(xc, yc, R, r, l):
    # set color
    turtle.color(random.random(),
                 random.random(),
                 random.random())

    # get ratio if radii
    k = r/R

    # got to first point
    turtle.up()
    a = 0.0
    x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
    y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
    turtle.setpos(xc + x, yc + y)
    turtle.down()
    
    # draw rest of points
    theta = 2.0*math.pi*10
    for a in np.linspace(0, theta, 10*100):
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        turtle.setpos(xc + x, yc + y)
    

# draw random spirographs one after the other
def drawRandomSpiros():
    xc, yc = 0, 0
    
    while True:
         R = random.randint(150, 250)
         r = random.randint(0, 90)
         k = r/R
         l = random.random()
         drawSpiro(xc, yc, R, r, l)
         turtle.clear()
         

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

  # set to 80% screen width
  turtle.setup(width=0.8)

  # set cursor shape
  turtle.shape('turtle')

  # set title
  turtle.title("Spirographs!")
  # add key handler for saving images
  turtle.onkey(saveDrawing, "s")
  # start listening 
  turtle.listen()

  # checks args and draw
  if args.sparams:
      params = [float(x) for x in args.sparams]
      # draw spirograph with given parameters
      drawSpiro(0, 0, *params)
  else:
      drawRandomSpiros()

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
