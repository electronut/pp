"""
psmain.py

Author: Mahesh Venkitachalam
 
Description: A particle system
"""

import sys
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *

import numpy    
from ps import ParticleSystem, Camera
from box import Box
import math
import glutils

class PSMaker:
    def __init__(self):
        self.camera = Camera([15.0, 0.0, 2.5],
                             [0.0, 0.0, 2.5],
                             [0.0, 0.0, 1.0])
        self.aspect = 1.0
        self.numP = 300
        self.t = 0
        # flag to rotate camera view
        self.rotate = True
        # initialize GLUT
        glutInit('Particle System')
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(500, 500)
        self.window = glutCreateWindow("Particle System")
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.draw)
        glutKeyboardFunc(self.keyPressed) # Checks for key strokes
        self.psys = ParticleSystem(self.numP)
        self.box = Box(1.0)
        glutTimerFunc(10, self.update, 0)
        glutMainLoop()


    def reshape(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        glutPostRedisplay()

    def keyPressed(self, *args):
        """key press handler"""
        if args[0] == '\x1b':
            sys.exit()
        elif args[0] == 'r':
            self.rotate = not self.rotate
        elif args[0] == 'b':
            # toggle billboarding
            self.psys.enableBillboard = not self.psys.enableBillboard
        elif args[0] == 'd':
            # toggle depth mask
            self.psys.disableDepthMask = not self.psys.disableDepthMask
        elif args[0] == 't':
            # toggle transparency
            self.psys.enableBlend = not self.psys.enableBlend

    def draw(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # render
        pMatrix = glutils.perspective(100.0, self.aspect, 0.1, 100.0)
        # modelview matrix
        mvMatrix = glutils.lookAt(self.camera.eye, self.camera.center, 
                                  self.camera.up)

        # draw non-transparent object first
        self.box.render(pMatrix, mvMatrix)

        # render
        self.psys.render(pMatrix, mvMatrix, self.camera)

        # swap buffers
        glutSwapBuffers()

    def update(self, *args):
        # inc time
        self.t += 10
        self.psys.step()
        # rotate eye
        if self.rotate:
            self.camera.rotate()
        # restart every 5 seconds 
        if not int(self.t) % 5000:
            self.psys.restart(self.numP)
        # set next timer - 10 milliseconds
        glutTimerFunc(10, self.update, 0)
        # redraw
        glutPostRedisplay()

# main() function
def main():
  # use sys.argv if needed
  print 'starting particle system...'
  prog = PSMaker()

# call main
if __name__ == '__main__':
  main()

