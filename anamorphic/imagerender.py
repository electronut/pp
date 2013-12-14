"""
imagerender.py

A class that renders an OpenGL scene to an image.

Author: Mahesh Venkitachalam
"""

import OpenGL
from OpenGL.GL import *
import Image

class ImageRender:
    """
    A class that renders an OpenGL scene to an image.
    """
    
    def __init__(self, width, height, texUnit):
        """Constructor for ImageRender"""
        self.width, self.height = width, height
        self.texUnit = texUnit
        self.reinit(width, height)

    def bind(self):
        """bind to ImageRender. All further GL calls will go to this FBO"""
        # render to FBO
        glBindFramebuffer(GL_FRAMEBUFFER, self.fboHandle)
        # set active texture
        glActiveTexture(self.texUnit)
        # bind to fbo1 texture
        glBindTexture(GL_TEXTURE_2D, self.texHandle)
    
    def unbind(self):
        """unbind from ImageRender"""
        # unbind texture
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

    def saveImage(self, imgFile):
        """write contents of FBO to given image file."""
        data = glReadPixels(0, 0, self.width, self.height, 
                            GL_RGBA, GL_UNSIGNED_BYTE)
        img = Image.frombuffer("RGBA", (self.width, self.height), 
                               data, "raw", "RGBA", 0, 0)
        img.save(imgFile)

    def reinit(self, width, height):

        # clear old
        #self.clearFBO()
        
        # create frame buffer object
        self.fboHandle = glGenFramebuffers(1)
        # create texture
        self.texHandle = glGenTextures(1)    
        # create depth buffer
        self.depthHandle = glGenRenderbuffers(1)

        # bind
        glBindFramebuffer(GL_FRAMEBUFFER, self.fboHandle)
    
        glActiveTexture(self.texUnit)
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
            print "fbo %d complete" % self.fboHandle
        elif status == GL_FRAMEBUFFER_UNSUPPORTED:
            print "fbo %d unsupported" % self.fboHandle
        else:
            print "fbo %d Error" % self.fboHandle
            
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

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
