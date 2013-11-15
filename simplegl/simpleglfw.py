"""
simpleglfw.py

Simple Python OpenGL program that uses PyOpenGL + GLFW to get an 
OpenGL 3.2 context.

Author: Mahesh Venkitachalam
"""

import OpenGL
from OpenGL.GL import *

import numpy, math, sys, os
import glutils

import cyglfw3 as glfw

strVS = """
#version 330 core

layout(location = 0) in vec3 aVert;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform vec4 uColor;
uniform float uTheta;

out vec4 vCol;
out vec2 vTexCoord;

void main() {
  // rotational transform
  mat4 rot =  mat4(
		vec4( cos(uTheta),  sin(uTheta), 0.0, 0.0),
		vec4(-sin(uTheta),  cos(uTheta), 0.0, 0.0),
	    vec4(0.0,         0.0,         1.0, 0.0),
	    vec4(0.0,         0.0,         0.0, 1.0)
	    );
  // transform vertex
  gl_Position = uPMatrix * uMVMatrix * rot * vec4(aVert, 1.0); 
  // set color
  vCol = vec4(uColor.rgb, 1.0);
  // set texture coord
  vTexCoord = aVert.xy + vec2(0.5, 0.5);
}
"""
strFS = """
#version 330 core

in vec4 vCol;
in vec2 vTexCoord;

uniform sampler2D tex2D;
uniform bool showCircle;

out vec4 fragColor;

void main() {
  if (showCircle) {
    // discard fragment outside circle
    if (distance(vTexCoord, vec2(0.5, 0.5)) > 0.5) {
      discard;
    }
    else {
      fragColor = texture(tex2D, vTexCoord);
    }
  }
  else {
     fragColor = texture(tex2D, vTexCoord);
  }
}
"""

class Scene:    
    """ OpenGL 3D scene class"""
    # initialization
    def __init__(self):
        # create shader
        self.program = glutils.loadShaders(strVS, strFS)

        glUseProgram(self.program)

        self.pMatrixUniform = glGetUniformLocation(self.program, 
                                                   'uPMatrix')
        self.mvMatrixUniform = glGetUniformLocation(self.program, 
                                                  "uMVMatrix")
        self.colorU = glGetUniformLocation(self.program, "uColor")

        # color
        self.col0 = [1.0, 0.0, 0.0, 1.0]

        # texture 
        self.tex2D = glGetUniformLocation(self.program, "tex2D")

        # define quad vertices 
        quadV = [
            -0.5, -0.5, 0.0, 
            0.5, -0.5, 0.0, 
            -0.5, 0.5, 0.0,
             0.5, 0.5, 0.0
            ]

        # set up vertex array object (VAO)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        # vertices
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        vertexData = numpy.array(quadV, numpy.float32)
        glBufferData(GL_ARRAY_BUFFER, 4*len(vertexData), vertexData, 
                     GL_STATIC_DRAW)
        # enable vertex array
        glEnableVertexAttribArray(0)
        # set buffer data
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        # unbind VAO
        glBindVertexArray(0)

        # time
        self.t = 0 

        # texture
        self.texId = glutils.loadTexture('test.png')

        # show circle?
        self.showCircle = False
        
    # step
    def step(self):
        # increment angle
        self.t = (self.t + 1) % 360
        # set shader angle in radians
        glUniform1f(glGetUniformLocation(self.program, 'uTheta'), 
                    math.radians(self.t))

    # render 
    def render(self, pMatrix, mvMatrix):        
        # use shader
        glUseProgram(self.program)
        
        # set proj matrix
        glUniformMatrix4fv(self.pMatrixUniform, 1, GL_FALSE, pMatrix)

        # set modelview matrix
        glUniformMatrix4fv(self.mvMatrixUniform, 1, GL_FALSE, mvMatrix)

        # show circle?
        glUniform1i(glGetUniformLocation(self.program, 'showCircle'), 
                    self.showCircle)

        # enable texture 
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texId)

        glUniform1i(self.tex2D, 0)

        # bind VAO
        glBindVertexArray(self.vao)
        # draw
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        # unbind VAO
        glBindVertexArray(0)


class RenderWindow:
    """GLFW Rendering window class"""
    def __init__(self):

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
        self.width, self.height = 640, 480
        self.aspect = self.width/float(self.height)
        self.win = glfw.CreateWindow(self.width, self.height, "test")
        # make context current
        glfw.MakeContextCurrent(self.win)
        
        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.5, 0.5,1.0)

        # set window callbacks
        glfw.SetMouseButtonCallback(self.win, self.onMouseButton)
        glfw.SetKeyCallback(self.win, self.onKeyboard)
        glfw.SetWindowSizeCallback(self.win, self.onSize)        

        # create 3D
        self.scene = Scene()

        # exit flag
        self.exitNow = False

        
    def onMouseButton(self, win, button, action, mods):
        #print 'mouse button: ', win, button, action, mods
        pass

    def onKeyboard(self, win, key, scancode, action, mods):
        #print 'keyboard: ', win, key, scancode, action, mods
        if action == glfw.PRESS:
            # ESC to quit
            if key == glfw.KEY_ESCAPE: 
                self.exitNow = True
            else:
                # toggle cut
                self.scene.showCircle = not self.scene.showCircle 
        
    def onSize(self, win, width, height):
        #print 'onsize: ', win, width, height
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)

    def run(self):
        # initializer timer
        glfw.SetTime(0.0)
        t = 0.0
        while not glfw.WindowShouldClose(self.win) and not self.exitNow:
            # update every x seconds
            currT = glfw.GetTime()
            if currT - t > 0.1:
                # update time
                t = currT
                # clear
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                
                # build projection matrix
                pMatrix = glutils.perspective(45.0, self.aspect, 0.1, 100.0)
                
                mvMatrix = glutils.lookAt([0.0, 0.0, -2.0], [0.0, 0.0, 0.0],
                                          [0.0, 1.0, 0.0])
                # render
                self.scene.render(pMatrix, mvMatrix)
                # step 
                self.scene.step()

                glfw.SwapBuffers(self.win)
                # Poll for and process events
                glfw.PollEvents()
        # end
        glfw.Terminate()

# main() function
def main():
    print 'starting simpleglfw...'    
    rw = RenderWindow()
    rw.run()

# call main
if __name__ == '__main__':
    main()
