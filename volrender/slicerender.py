"""
slicerender.py

Author: Mahesh Venkitachalam

This module has the classed and methods related to X Y Z slice rendering 
of a Volumetric data set.
"""

import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import numpy, math, sys 

import volreader, glutils

strVS = """
# version 330 core

in vec3 aVert;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;

uniform float uSliceFrac;
uniform int uSliceMode;

out vec3 texcoord;

void main() {

  // X-slice?
  if (uSliceMode == 0) {
    texcoord = vec3(uSliceFrac, aVert.x, 1.0-aVert.y);
  }
  // Y-slice?
  else if (uSliceMode == 1) {
    texcoord = vec3(aVert.x, uSliceFrac, 1.0-aVert.y);
  }
  // Z-slice
  else {
    texcoord = vec3(aVert.x, 1.0-aVert.y, uSliceFrac);
  }

  // calculate transformed vertex
  gl_Position = uPMatrix * uMVMatrix * vec4(aVert, 1.0); 
}
"""
strFS = """
# version 330 core

in vec3 texcoord;

uniform sampler3D tex;

out vec4 fragColor;

void main() {
  // look up color in texture
  vec4 col = texture(tex, texcoord);
  fragColor = col.rrra;
}

"""

class SliceRender:
    # slice modes
    XSLICE, YSLICE, ZSLICE = 0, 1, 2

    def __init__(self, width, height, volume):
        """SliceRender constructor"""
        self.width = width
        self.height = height
        self.aspect = width/float(height)

        # slice mode
        self.mode = SliceRender.ZSLICE

        # create shader
        self.program = glutils.loadShaders(strVS, strFS)

        glUseProgram(self.program)

        self.pMatrixUniform = glGetUniformLocation(self.program, b'uPMatrix')
        self.mvMatrixUniform = glGetUniformLocation(self.program, 
                                                  b"uMVMatrix")

        # attributes
        self.vertIndex = glGetAttribLocation(self.program, b"aVert")
 
        # set up vertex array object (VAO)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # define quad vertices 
        vertexData = numpy.array([ 0.0, 1.0, 0.0, 
                                   0.0, 0.0, 0.0, 
                                   1.0, 1.0, 0.0,
                                   1.0, 0.0, 0.0], numpy.float32)
        # vertex buffer
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, 4*len(vertexData), vertexData, 
                     GL_STATIC_DRAW)
        # enable arrays
        glEnableVertexAttribArray(self.vertIndex)
        # set buffers 
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, 0, None)

        # unbind VAO
        glBindVertexArray(0)

        # load texture
        self.texture, self.Nx, self.Ny, self.Nz = volume

        # current slice index
        self.currSliceIndex = int(self.Nz/2);
        self.currSliceMax = self.Nz;


    def reshape(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        
    def draw(self):
        # clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # build projection matrix
        pMatrix = glutils.ortho(-0.6, 0.6, -0.6, 0.6, 0.1, 100.0)
        # modelview matrix
        mvMatrix = numpy.array([1.0, 0.0, 0.0, 0.0, 
                                0.0, 1.0, 0.0, 0.0, 
                                0.0, 0.0, 1.0, 0.0, 
                                -0.5, -0.5, -1.0, 1.0], numpy.float32)        
        # use shader
        glUseProgram(self.program)
        
        # set proj matrix
        glUniformMatrix4fv(self.pMatrixUniform, 1, GL_FALSE, pMatrix)

        # set modelview matrix
        glUniformMatrix4fv(self.mvMatrixUniform, 1, GL_FALSE, mvMatrix)

        # set current slice fraction
        glUniform1f(glGetUniformLocation(self.program, b"uSliceFrac"), 
                    float(self.currSliceIndex)/float(self.currSliceMax))
        # set current slice mode
        glUniform1i(glGetUniformLocation(self.program, b"uSliceMode"), 
                    self.mode)
        
        # enable texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_3D, self.texture)
        glUniform1i(glGetUniformLocation(self.program, b"tex"), 0)

        # bind VAO
        glBindVertexArray(self.vao)
        # draw
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        # unbind VAO
        glBindVertexArray(0)

    def keyPressed(self, key):
        """key press handler"""
        if key == 'x':
            self.mode = SliceRender.XSLICE
            # reset slice index
            self.currSliceIndex = int(self.Nx/2)
            self.currSliceMax = self.Nx
        elif key == 'y':
            self.mode = SliceRender.YSLICE
            # reset slice index
            self.currSliceIndex = int(self.Ny/2)
            self.currSliceMax = self.Ny
        elif key == 'z':
            self.mode = SliceRender.ZSLICE
            # reset slice index
            self.currSliceIndex = int(self.Nz/2)
            self.currSliceMax = self.Nz
        elif key == 'l':
            self.currSliceIndex = (self.currSliceIndex + 1) % self.currSliceMax
        elif key == 'r':
            self.currSliceIndex = (self.currSliceIndex - 1) % self.currSliceMax
            
    def close(self):
        pass
