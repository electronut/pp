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
from fractions import gcd

# A class that draws a spirograph
class Spiro:
    # constructor
    def __init__(self, xc, yc, col, R, r, l):
        # spirograph parameters
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col
        # create own turtle
        self.t = turtle.Turtle()
        # set cursor shape
        self.t.shape('turtle')
        
        # set step
        self.step = math.radians(5.0)

        # reduce r/R to smallest form by dividing with GCD
        gcdVal = gcd(self.r, self.R)
        self.nRot = self.r//gcdVal
        self.nRev = self.R//gcdVal
        print(gcdVal)
        # set initial angle
        self.a = 0.0

        # get ratio of radii
        k = self.k = r/R

        # set color
        self.t.color(*col)

        # go to first point
        self.t.up()
        a = 0.0
        x = self.R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(xc + x, yc + y)
        self.t.down()

    # draw the whole thing
    def draw(self):
        # draw rest of points
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360*self.nRot + 5, 5):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)

    # update by one step
    def update(self):
        # increment angle
        self.a += self.step
        # draw
        a, R, k, l = self.a, self.R, self.k, self.l
        x = self.R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)

    # clear everything
    def clear(self):
        self.t.clear()

# A class for animating spirographs
class SpiroAnimator:
    # constructor
    def __init__(self):
        # list of spiros
        self.spiros = []
        # timer value in milliseconds
        self.deltaT = 10
        # restart time in milliseconds
        self.restartT = 10000
        # running time of current drawing
        self.currT = 0 
        # create spiro objects
        self.restart()
        # start update
        self.update()

    # restart sprio drawing
    def restart(self):
        # clear everything
        for spiro in self.spiros:
            spiro.clear()     

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
            spiro = Spiro(xc, yc, col, R, r, l)
            # add to list 
            self.spiros.append(spiro)

    def update(self):
        # update all spiros
        for spiro in self.spiros:
            spiro.update()       
        # inc running time
        self.currT += self.deltaT
        # restart 
        if self.currT >= self.restartT:
            self.currT = 0
            self.restart()
        # call timer again
        turtle.ontimer(self.update, self.deltaT)

    # toggle turtle on/off
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()
            
# save spiros to image
def saveDrawing():
    # hide turtle
    turtle.hideturtle()
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
    # show turtle
    turtle.showturtle()

# toggle turtle on/off
def toggleTurtle():
    if turtle.isvisible():
        turtle.hideturtle()
    else:
        turtle.showturtle()

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

    # hide main turtle cursor
    turtle.hideturtle()

    # checks args and draw
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # add key handler to toggle turtle cursor
        turtle.onkey(toggleTurtle, "t")
        # draw spirograph with given parameters
        col = (random.random(),
               random.random(),
               random.random())
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create animator object
        spiroAnim = SpiroAnimator()
        # add key handler to toggle turtle cursor
        turtle.onkey(spiroAnim.toggleTurtles, "t")

    # start turtle main loop
    turtle.mainloop()

# call main
if __name__ == '__main__':
    main()

"""
- HIDE turtle - key

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
