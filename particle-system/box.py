"""
box.py

Draws the cone and floor used in the "fountain" Paticle System.

Author: Mahesh Venkitachalam
"""

import sys, random, math
import OpenGL
from OpenGL.GL import *
import numpy
import glutils

strVS = """
attribute vec3 aVert;
uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
varying vec4 vCol;

void main() {
    // apply transformations
	gl_Position = uPMatrix * uMVMatrix * vec4(aVert, 1.0); 
    // set color
    vCol = vec4(0.8, 0.0, 0.0, 1.0);
}
"""

strFS = """
varying vec4 vCol;

void main() {
    // use vertex color
    gl_FragColor = vCol;
}
"""


class Box:
    def __init__(self, side):
        self.side = side

        # load shaders
        self.program = glutils.loadShaders(strVS, strFS)
        glUseProgram(self.program)
        
        s = side/2.0
        vertices = [
            -s, s, -s, 
             -s, -s, -s,
             s, -s, -s,
             s, s, -s,

             -s, s, s, 
             -s, -s, s,
             s, -s, s,
             s, s, s,

             -s, -s, s, 
             -s, -s, -s,
             s, -s, -s,
             s, -s, s,

             -s, s, s, 
             -s, s, -s,
             s, s, -s,
             s, s, s,

             -s, -s, s, 
             -s, -s, -s,
             -s, s, -s,
             -s, s, s,
             
             s, -s, s, 
             s, -s,-s,
             s, s, -s,
             s, s, s,
             ]
                
        # set up VBOs
        vertexData = numpy.array(vertices, numpy.float32)
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, 4*len(vertexData), vertexData, 
                     GL_STATIC_DRAW)

        # attributes
        self.vertIndex = glGetAttribLocation(self.program, "aVert")

    def render(self, pMatrix, mvMatrix):

        # use shader
        glUseProgram(self.program)
        
        # set proj matrix
        glUniformMatrix4fv(glGetUniformLocation(self.program, 'uPMatrix'), 
                           1, GL_FALSE, pMatrix)
        
        # set modelview matrix
        glUniformMatrix4fv(glGetUniformLocation(self.program, 'uMVMatrix'), 
                           1, GL_FALSE, mvMatrix)

        #enable arrays
        glEnableVertexAttribArray(self.vertIndex)

        # set buffers 
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, 0, None)

        # draw
        glDrawArrays(GL_QUADS, 0, 24)

        # disable arrays
        glDisableVertexAttribArray(self.vertIndex)

