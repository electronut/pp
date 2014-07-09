"""
volrender.py

Author: Mahesh Venkitachalam

A Ray Casting Volume Renderer for medical data visualization.

"""

import sys, argparse, os
from slicerender import *
from raycast import *
import glfw

class RenderWin:
    """GLFW Rendering window class"""
    def __init__(self, imageDir):
        
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
        glfw.glfwWindowHint(glfw.GLFW_OPENGL_PROFILE, glfw.GLFW_OPENGL_CORE_PROFILE)

        # make a window
        self.width, self.height = 512, 512
        self.aspect = self.width/float(self.height)
        self.win = glfw.glfwCreateWindow(self.width, self.height, b"volrender")
        # make context current
        glfw.glfwMakeContextCurrent(self.win)
        
        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 0.0)

        # set window callbacks
        glfw.glfwSetMouseButtonCallback(self.win, self.onMouseButton)
        glfw.glfwSetKeyCallback(self.win, self.onKeyboard)
        glfw.glfwSetWindowSizeCallback(self.win, self.onSize)

        # load volume data
        self.volume =  volreader.loadVolume(imageDir)
        # create renderer
        self.renderer = RayCastRender(self.width, self.height, self.volume)

        # exit flag
        self.exitNow = False
        
    def onMouseButton(self, win, button, action, mods):
        #print 'mouse button: ', win, button, action, mods
        pass

    def onKeyboard(self, win, key, scancode, action, mods):
        #print 'keyboard: ', win, key, scancode, action, mods
        # ESC to quit
        if key is glfw.GLFW_KEY_ESCAPE:
            self.renderer.close()
            self.exitNow = True
        else:
            if action is glfw.GLFW_PRESS or action is glfw.GLFW_REPEAT:
                if key == glfw.GLFW_KEY_V:
                    # toggle render mode
                    if isinstance(self.renderer, RayCastRender):
                        self.renderer = SliceRender(self.width, self.height, 
                                                    self.volume)
                    else:
                        self.renderer = RayCastRender(self.width, self.height, 
                                                      self.volume)
                    # call reshape on renderer
                    self.renderer.reshape(self.width, self.height)
                else:
                    # send key press to renderer
                    keyDict = {glfw.GLFW_KEY_X : 'x', glfw.GLFW_KEY_Y: 'y', 
                               glfw.GLFW_KEY_Z: 'z', 
                               glfw.GLFW_KEY_LEFT: 'l', glfw.GLFW_KEY_RIGHT: 'r'}
                    try:
                        self.renderer.keyPressed(keyDict[key])
                    except:
                        pass

    def onSize(self, win, width, height):
        #print 'onsize: ', win, width, height
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)
        self.renderer.reshape(width, height)

    def run(self):
        # start loop
        while not glfw.glfwWindowShouldClose(self.win) and not self.exitNow:
            # render
            self.renderer.draw()
            # swap buffers
            glfw.glfwSwapBuffers(self.win)
            # wait for events
            glfw.glfwWaitEvents()
        # end
        glfw.glfwTerminate()

# main() function
def main():
  print('starting volrender...')
  # create parser
  parser = argparse.ArgumentParser(description="Volume Rendering...")
  # add expected arguments
  parser.add_argument('--dir', dest='imageDir', required=True)
  # parse args
  args = parser.parse_args()

  # create render window
  rwin = RenderWin(args.imageDir)
  rwin.run()

# call main
if __name__ == '__main__':
  main()
