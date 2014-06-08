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


# A class that draws a spirograph
class Spiro:
    # constructor
    def __init__(self, xc, yc, R, r, l, col):
        # spirograph parameters
        self.xc = xc
        self.yc = yc
        self.R = R
        self.r = r
        self.l = l
        self.col = col
        # create own turtle
        self.t = turtle.Turtle()
        # set cursor shape
        self.t.shape('turtle')
        
        # set step
        self.step = math.radians(5.0)
        # set initial angle
        self.a = 0.0

        # get ratio of radii
        k = self.k = r/R

        # set color
        self.t.color(*col)

        # go to first point
        self.t.up()
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(xc + x, yc + y)
        self.t.down()
        
    # update by one step
    def update(self):
        # increment angle
        self.a += self.step
        # draw
        a, R, k, l = self.a, self.R, self.k, self.l
        x = self.R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)

# A class for animating spirographs
class SpiroAnimator:
    # constructor
    def __init__(self):
        # create spiro objects
        self.spiros = []
        width = turtle.window_width()
        height = turtle.window_height()
        for i in range(4):
            R = random.randint(150, 250)
            r = random.randint(0, 90)
            l = random.random()
            xc = random.randint(0, width/4)
            yc = random.randint(0, height/4)
            col = (random.random(),
                   random.random(),
                   random.random())
            # create a spiro
            spiro = Spiro(xc, yc, R, r, l, col)
            # add to list 
            self.spiros.append(spiro)
        # start update
        self.update()

    def update(self):
        # update all spiros
        for spiro in self.spiros:
            spiro.update()
        # call timer again
        turtle.ontimer(self.update, 1)

    
# draw spirograph
def drawSpiro(t, xc, yc, R, r, l):
    # set color
    t.color(random.random(),
                 random.random(),
                 random.random())

    # get ratio if radii
    k = r/R

    # got to first point
    t.up()
    a = 0.0
    x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
    y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
    t.setpos(xc + x, yc + y)
    t.down()
    
    # draw rest of points
    theta = 2.0*math.pi*10
    for a in np.linspace(0, theta, 10*100):
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        t.setpos(xc + x, yc + y)
    

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
      #drawSpiro(0, 0, *params)
      spiro = Spiro(0, 0, *params)
      spiro.draw()
  else:
      spiroAnim = SpiroAnimator()

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
