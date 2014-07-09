"""
psmain.py

Author: Mahesh Venkitachalam
 
Description: A particle system
"""

import sys, os, math, numpy
import OpenGL
from OpenGL.GL import *
import numpy    
from ps import ParticleSystem, Camera
from box import Box
import glutils
import glfw

class PSMaker:
    """GLFW Rendering window class for Particle System"""
    def __init__(self):
        self.camera = Camera([15.0, 0.0, 2.5],
                             [0.0, 0.0, 2.5],
                             [0.0, 0.0, 1.0])
        self.aspect = 1.0
        self.numP = 300
        self.t = 0
        # flag to rotate camera view
        self.rotate = True

        # save current working directory
        cwd = os.getcwd()

        # initialize glfw - this changes cwd
        glfw.glfwInit()
        
        # restore cwd
        os.chdir(cwd)

        # version hints
        glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.glfwWindowHint(glfw.GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.glfwWindowHint(glfw.GLFW_OPENGL_PROFILE, 
                            glfw.GLFW_OPENGL_CORE_PROFILE)

        # make a window
        self.width, self.height = 640, 480
        self.aspect = self.width/float(self.height)
        self.win = glfw.glfwCreateWindow(self.width, self.height, 
                                     b"Particle System")
        # make context current
        glfw.glfwMakeContextCurrent(self.win)
        
        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.2, 0.2, 0.2,1.0)

        # set window callbacks
        glfw.glfwSetMouseButtonCallback(self.win, self.onMouseButton)
        glfw.glfwSetKeyCallback(self.win, self.onKeyboard)
        glfw.glfwSetWindowSizeCallback(self.win, self.onSize)        

        # create 3D
        self.psys = ParticleSystem(self.numP)
        self.box = Box(1.0)

        # exit flag
        self.exitNow = False

        
    def onMouseButton(self, win, button, action, mods):
        #print 'mouse button: ', win, button, action, mods
        pass

    def onKeyboard(self, win, key, scancode, action, mods):
        #print 'keyboard: ', win, key, scancode, action, mods
        if action == glfw.GLFW_PRESS:
            # ESC to quit
            if key == glfw.GLFW_KEY_ESCAPE: 
                self.exitNow = True
            elif key == glfw.GLFW_KEY_R:
                self.rotate = not self.rotate
            elif key == glfw.GLFW_KEY_B:
                # toggle billboarding
                self.psys.enableBillboard = not self.psys.enableBillboard
            elif key == glfw.GLFW_KEY_D:
                # toggle depth mask
                self.psys.disableDepthMask = not self.psys.disableDepthMask
            elif key == glfw.GLFW_KEY_T:
                # toggle transparency
                self.psys.enableBlend = not self.psys.enableBlend
        
    def onSize(self, win, width, height):
        #print 'onsize: ', win, width, height
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)

    def step(self):
        # inc time
        self.t += 10
        self.psys.step()
        # rotate eye
        if self.rotate:
            self.camera.rotate()
        # restart every 5 seconds 
        if not int(self.t) % 5000:
            self.psys.restart(self.numP)

    def run(self):
        # initializer timer
        glfw.glfwSetTime(0)
        t = 0.0
        while not glfw.glfwWindowShouldClose(self.win) and not self.exitNow:
            # update every x seconds
            currT = glfw.glfwGetTime()
            if currT - t > 0.01:
                # update time
                t = currT

                # clear
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

                # step 
                self.step()

                glfw.glfwSwapBuffers(self.win)
                # Poll for and process events
                glfw.glfwPollEvents()
        # end
        glfw.glfwTerminate()

# main() function
def main():
  # use sys.argv if needed
  print('starting particle system...')
  prog = PSMaker()
  prog.run()

# call main
if __name__ == '__main__':
  main()

