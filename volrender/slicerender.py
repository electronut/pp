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
uniform vec4 uColor;

uniform int uCurrSliceIndex;
uniform int uSliceMode;
uniform int uCurrSliceMax;
uniform vec3 uTexCoord;

out vec4 vCol;
out vec3 texcoord;

void main() {
  gl_Position = uPMatrix * uMVMatrix * vec4(aVert, 1.0); 
  // set color
  vCol = vec4(uColor.rgb, 1.0);

  float tc = (0.5 + float(uCurrSliceIndex)) / float(uCurrSliceMax);

  if (uSliceMode == 0) {
    texcoord = vec3(tc, aVert.xy);
  }
  else if (uSliceMode == 1) {
    texcoord = vec3(aVert.x, tc, aVert.y);
  }
  else {
    texcoord = vec3(aVert.xy, tc);
  }
}
"""
strFS = """
# version 330 core

in vec4 vCol;
in vec3 texcoord;

uniform sampler3D texture;

out vec4 fragColor;

void main() {
  // use vertex color
  //gl_FragColor = vCol;
  vec4 col = texture(texture, texcoord);
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
        """
        self.program = compileProgram(compileShader(strVS,
                                                    GL_VERTEX_SHADER),
                                      compileShader(strFS,
                                                    GL_FRAGMENT_SHADER))
                                                    """
        self.program = glutils.loadShaders(strVS, strFS)

        glUseProgram(self.program)

        self.pMatrixUniform = glGetUniformLocation(self.program, 'uPMatrix')
        self.mvMatrixUniform = glGetUniformLocation(self.program, 
                                                  "uMVMatrix")
        self.colorU = glGetUniformLocation(self.program, "uColor")

        # attributes
        self.vertIndex = glGetAttribLocation(self.program, "aVert")

        # color
        self.col0 = [1.0, 1.0, 0.0, 1.0]

 
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
        #self.texture = volreader.loadTexture('test.png')
        self.texture, self.Nx, self.Ny, self.Nz = volume

        # current slice index
        self.currSliceIndex = self.Nz/2;
        self.currSliceMax = self.Nz;


    def reshape(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width/float(height)

    # step
    def step(self):
        pass

    # render 
    def render(self, pMatrix, mvMatrix):        
        # use shader
        glUseProgram(self.program)
        
        # set proj matrix
        glUniformMatrix4fv(self.pMatrixUniform, 1, GL_FALSE, pMatrix)

        # set modelview matrix
        glUniformMatrix4fv(self.mvMatrixUniform, 1, GL_FALSE, mvMatrix)

        # set color
        glUniform4fv(self.colorU, 1, self.col0)

        # set current slice params
        glUniform1i(glGetUniformLocation(self.program, "uCurrSliceIndex"), 
                    self.currSliceIndex)
        glUniform1i(glGetUniformLocation(self.program, "uCurrSliceMax"), 
                    self.currSliceMax)
        glUniform1i(glGetUniformLocation(self.program, "uSliceMode"), 
                    self.mode)

        # enable texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_3D, self.texture)
        glUniform1i(glGetUniformLocation(self.program, "texture"), 0)

        # bind VAO
        glBindVertexArray(self.vao)
        # draw
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        # unbind VAO
        glBindVertexArray(0)
        
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # build projection matrix
        a = self.aspect
        pMatrix = glutils.perspective(45.0, self.aspect, 0.1, 100.0)
        
        # modelview matrix
        mvMatrix = numpy.array([1.0, 0.0, 0.0, 0.0, 
                                0.0, 1.0, 0.0, 0.0, 
                                0.0, 0.0, 1.0, 0.0, 
                                -0.5, -0.5, -1.0, 1.0], numpy.float32)
        
        # render
        self.render(pMatrix, mvMatrix)

    def keyPressed(self, key):
        """key press handler"""
        if key == 'x':
            self.mode = SliceRender.XSLICE
            # reset slice index
            self.currSliceIndex = self.Nx/2
            self.currSliceMax = self.Nx
        elif key == 'y':
            self.mode = SliceRender.YSLICE
            # reset slice index
            self.currSliceIndex = self.Ny/2
            self.currSliceMax = self.Ny
        elif key == 'z':
            self.mode = SliceRender.ZSLICE
            # reset slice index
            self.currSliceIndex = self.Nz/2
            self.currSliceMax = self.Nz
        elif key == 'a':
            self.currSliceIndex = (self.currSliceIndex + 1) % self.currSliceMax
        elif key == 's':
            self.currSliceIndex = (self.currSliceIndex - 1) % self.currSliceMax
            
    def close(self):
        pass
