"""
volrender.py

Author: Mahesh Venkitachalam

A Ray Casting Volume Renderer for medical data visualization.

"""

import sys, argparse, os
from slicerender import *
from raycast import *
import cyglfw3 as glfw

class RenderWin:
    """GLFW Rendering window class"""
    def __init__(self, imageDir):
        
        # save current working directory
        cwd = os.getcwd()

        # initialize glfw - this changes cwd
        glfw.Init()
        
        # restore cwd
        os.chdir(cwd)

        # version hints
        glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.WindowHint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.WindowHint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # make a window
        self.width, self.height = 512, 512
        self.aspect = self.width/float(self.height)
        self.win = glfw.CreateWindow(self.width, self.height, b"volrender")
        # make context current
        glfw.MakeContextCurrent(self.win)
        
        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 0.0)

        # set window callbacks
        glfw.SetMouseButtonCallback(self.win, self.onMouseButton)
        glfw.SetKeyCallback(self.win, self.onKeyboard)
        glfw.SetWindowSizeCallback(self.win, self.onSize)

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
        if key is glfw.KEY_ESCAPE:
            self.renderer.close()
            self.exitNow = True
        else:
            if action is glfw.PRESS or action is glfw.REPEAT:
                if key == glfw.KEY_V:
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
                    keyDict = {glfw.KEY_X : 'x', glfw.KEY_Y: 'y', 
                               glfw.KEY_Z: 'z', 
                               glfw.KEY_LEFT: 'l', glfw.KEY_RIGHT: 'r'}
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
        while not glfw.WindowShouldClose(self.win) and not self.exitNow:
            # render
            self.renderer.draw()
            # swap buffers
            glfw.SwapBuffers(self.win)
            # wait for events
            glfw.WaitEvents()
        # end
        glfw.Terminate()

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
