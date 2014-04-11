"""
raycube.py

Author: Mahesh Venkitachalam

Generates texture that has the cube/ray computation.
"""

import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *

import numpy, math, sys 
import volreader, glutils

strVS = """
#version 330 core

layout(location = 1) in vec3 cubePos;
layout(location = 2) in vec3 cubeCol;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
out vec4 vColor;

void main()
{
    // set back face color
    vColor = vec4(cubeCol.rgb, 1.0); 
    
    // transformed position
    vec4 newPos = vec4(cubePos.xyz, 1.0);
    
    // set position
    gl_Position = uPMatrix * uMVMatrix * newPos; 

}
"""
strFS = """
#version 330 core

in vec4 vColor;
out vec4 fragColor;

void main()
{
    fragColor = vColor;
}
"""

class RayCube:
    """class used to generate rays used in ray casting"""
    
    def __init__(self, width, height):
        """RayCube constructor"""

        # set dims
        self.width, self.height = width, height

        # create shader
        self.program = glutils.loadShaders(strVS, strFS)

        # cube vertices
        vertices = numpy.array([
                0.0, 0.0, 0.0, 
                1.0, 0.0, 0.0, 
                1.0, 1.0, 0.0, 
                0.0, 1.0, 0.0, 
                0.0, 0.0, 1.0,
                1.0, 0.0, 1.0, 
                1.0, 1.0, 1.0, 
                0.0, 1.0, 1.0 
                ], numpy.float32)
        # cube colors
        colors = numpy.array([
                0.0, 0.0, 0.0, 
                1.0, 0.0, 0.0,
                1.0, 1.0, 0.0, 
                0.0, 1.0, 0.0,
                0.0, 0.0, 1.0,
                1.0, 0.0, 1.0, 
                1.0, 1.0, 1.0, 
                0.0, 1.0, 1.0 
                ], numpy.float32)

        # individual triangles
        indices = numpy.array([ 
                4, 5, 7, 
                7, 5, 6,
                5, 1, 6, 
                6, 1, 2, 
                1, 0, 2, 
                2, 0, 3,
                0, 4, 3, 
                3, 4, 7, 
                6, 2, 7, 
                7, 2, 3, 
                4, 0, 5, 
                5, 0, 1
                ], numpy.int16)
        
        self.nIndices = indices.size

        # set up vertex array object (VAO)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        #vertex buffer
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, 4*len(vertices), vertices, GL_STATIC_DRAW)
 
        # vertex buffer - color
        self.colorBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorBuffer)
        glBufferData(GL_ARRAY_BUFFER, 4*len(colors), colors, GL_STATIC_DRAW);
    
        # index buffer
        self.indexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indexBuffer);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 2*len(indices), indices, 
                     GL_STATIC_DRAW)
        
        # enable attrs using the layout indices in shader
        aPosLoc = 1
        aColorLoc = 2

        # bind buffers:
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
    
        # vertex
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glVertexAttribPointer(aPosLoc, 3, GL_FLOAT, GL_FALSE, 0, None)

        # color
        glBindBuffer(GL_ARRAY_BUFFER, self.colorBuffer)
        glVertexAttribPointer(aColorLoc, 3, GL_FLOAT, GL_FALSE, 0, None)
        # index
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indexBuffer)
        
        # unbind VAO
        glBindVertexArray(0)

        # FBO
        self.initFBO()

    def renderBackFace(self, pMatrix, mvMatrix):
        """renders back-face of ray-cube to a texture and returns it"""
        # render to FBO
        glBindFramebuffer(GL_FRAMEBUFFER, self.fboHandle)
        # set active texture
        glActiveTexture(GL_TEXTURE0)
        # bind to fbo1 texture
        glBindTexture(GL_TEXTURE_2D, self.texHandle)

        # render cube with face culling enabled
        self.renderCube(pMatrix, mvMatrix, self.program, True)
        
        # unbind texture
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

        # return texture id 
        return self.texHandle

    def renderFrontFace(self, pMatrix, mvMatrix, program):
        """render front face of ray-cube"""
        # no face culling
        self.renderCube(pMatrix, mvMatrix, program, False)

    def renderCube(self, pMatrix, mvMatrix, program, cullFace):
        """render cube use face culling if flag set"""
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # set shader program
        glUseProgram(program)
        
        # set proj matrix
        glUniformMatrix4fv(glGetUniformLocation(program, b'uPMatrix'), 
                           1, GL_FALSE, pMatrix)

        # set modelview matrix
        glUniformMatrix4fv(glGetUniformLocation(program, b'uMVMatrix'), 
                           1, GL_FALSE, mvMatrix)
 
        # enable face culling
        glDisable(GL_CULL_FACE)
        if cullFace:
            glFrontFace(GL_CCW)
            glCullFace(GL_FRONT)
            glEnable(GL_CULL_FACE)

        # bind VAO
        glBindVertexArray(self.vao)

        # animated slice
        glDrawElements(GL_TRIANGLES, self.nIndices, 
                       GL_UNSIGNED_SHORT, None)

        # unbind VAO
        glBindVertexArray(0)

        # reset cull face
        if cullFace:
            # disable face culling
            glDisable(GL_CULL_FACE)

    
    def reshape(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        # recreate FBO
        self.clearFBO()
        self.initFBO()
        
    def initFBO(self): 
        # create frame buffer object
        self.fboHandle = glGenFramebuffers(1)
        # create texture
        self.texHandle = glGenTextures(1)    
        # create depth buffer
        self.depthHandle = glGenRenderbuffers(1)

        # bind
        glBindFramebuffer(GL_FRAMEBUFFER, self.fboHandle)
    
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texHandle)
    
        # Set a few parameters to handle drawing the image at 
        # lower and higher sizes than original
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR) 
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        # set up texture
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 
                     0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        
        # bind texture to FBO
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, 
                               GL_TEXTURE_2D, self.texHandle, 0)
        
        # bind
        glBindRenderbuffer(GL_RENDERBUFFER, self.depthHandle)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, 
                              self.width, self.height)
    
        # bind depth buffer to FBO
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, 
                                  GL_RENDERBUFFER, self.depthHandle)
        # check status
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status == GL_FRAMEBUFFER_COMPLETE:
            pass
            #print "fbo %d complete" % self.fboHandle
        elif status == GL_FRAMEBUFFER_UNSUPPORTED:
            print("fbo %d unsupported" % self.fboHandle)
        else:
            print("fbo %d Error" % self.fboHandle)
            
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        return

    def clearFBO(self):
        """clears old FBO"""
        # delete FBO
        if glIsFramebuffer(self.fboHandle):
            glDeleteFramebuffers(int(self.fboHandle))
    
        # delete texture
        if glIsTexture(self.texHandle):
            glDeleteTextures(int(self.texHandle))
            

    def close(self):
        """call this to free up OpenGL resources"""
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
    
        # delete FBO
        if glIsFramebuffer(self.fboHandle):
            glDeleteFramebuffers(int(self.fboHandle))
    
        # delete texture
        if glIsTexture(self.texHandle):
            glDeleteTextures(int(self.texHandle))

        # delete render buffer
        """
        if glIsRenderbuffer(self.depthHandle):
            glDeleteRenderbuffers(1, int(self.depthHandle))
            """
        # delete buffers
        """
        glDeleteBuffers(1, self._vertexBuffer)
        glDeleteBuffers(1, &_indexBuffer)
        glDeleteBuffers(1, &_colorBuffer)
        """
