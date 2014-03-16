"""
raycast.py

Author: Mahesh Venkitachalam

This module has the classed and methods related to Volume rendering using 
the Ray Casting method.
"""


import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *

import numpy as np
import math, sys 

import raycube, glutils, volreader

strVS = """
#version 330 core

layout(location = 1) in vec3 cubePos;
layout(location = 2) in vec3 cubeCol;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;

out vec4 vColor;

void main()
{    
    // set position
    gl_Position = uPMatrix * uMVMatrix * vec4(cubePos.xyz, 1.0);

    // set color
    vColor = vec4(cubeCol.rgb, 1.0);
}
"""
strFS = """
#version 330 core

in vec4 vColor;

uniform sampler2D texBackFaces;
uniform sampler3D texVolume;
uniform vec2 uWinDims;

out vec4 fragColor;

void main()
{
    // start of ray
    vec3 start = vColor.rgb;

    // calculate texture coords at fragment, which is a 
    // fraction of window coords
    vec2 texc = gl_FragCoord.xy/uWinDims.xy;

    // get end of ray = back-face color
    vec3 end = texture(texBackFaces, texc).rgb;

    // calculate ray direction
    vec3 dir = end - start;

    // normalized ray direction
    vec3 norm_dir = normalize(dir);

    // the length from front to back is calculated and 
    // used to terminate the ray
    float len = length(dir.xyz);

    // ray step size
    float stepSize = 0.01;

    // X-Ray projection
    vec4 dst = vec4(0.0);
       
    // step through the ray
    for(float t = 0.0; t < len; t += stepSize) {

        // set position to end point of ray
        vec3 samplePos = start + t*norm_dir;

        // get texture value at position
        float val = texture(texVolume, samplePos).r;
        vec4 src = vec4(val);

        // set opacity
        src.a *= 0.1; 
        src.rgb *= src.a;

        // blend with previous value
        dst = (1.0 - dst.a)*src + dst;		
            
        // exit loop when alpha exceeds threshold
        if(dst.a >= 0.95)
            break;
    }
        
    // set fragment color
    fragColor =  dst;   
}
"""

class Camera:
    """helper class for viewing"""
    def __init__(self):
        self.r = 1.5
        self.theta = 0
        self.center = [0.5, 0.5, 0.5]
        self.eye = [0.5 + self.r, 0.5, 0.5]
        self.up = [0.0, 0.0, 1.0]

    def rotate(self, clockWise):
        """rotate eye by one step"""
        if clockWise:
            self.theta = (self.theta + 5) % 360
        else:
            self.theta = (self.theta - 5) % 360
        # recalculate eye
        self.eye = [0.5 + self.r*math.cos(math.radians(self.theta)), 
                    0.5 + self.r*math.sin(math.radians(self.theta)), 
                    0.5]

class RayCastRender:
    """class that does Ray Casting"""
    
    def __init__(self, width, height, volume):
        """RayCastRender constr"""
        
        # create RayCube object
        self.raycube = raycube.RayCube(width, height)
        
        # set dims
        self.width = width
        self.height = height
        self.aspect = width/float(height)

        # create shader
        self.program = glutils.loadShaders(strVS, strFS)
        # texture
        self.texVolume, self.Nx, self.Ny, self.Nz = volume
        
        # initialize camera
        self.camera = Camera()
        
    def draw(self):

        # build projection matrix
        pMatrix = glutils.perspective(45.0, self.aspect, 0.1, 100.0)
       
        # modelview matrix
        mvMatrix = glutils.lookAt(self.camera.eye, self.camera.center, 
                                  self.camera.up)
        # render
        
        # generate ray-cube back-face texture
        texture = self.raycube.renderBackFace(pMatrix, mvMatrix)
        
        # set shader program
        glUseProgram(self.program)

        # set window dimensions
        glUniform2f(glGetUniformLocation(self.program, b"uWinDims"),
                    float(self.width), float(self.height))

        # texture unit 0 - back-faces of cube
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glUniform1i(glGetUniformLocation(self.program, b"texBackFaces"), 0)
        
        # texture unit 1 - 3D volume texture
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_3D, self.texVolume)
        glUniform1i(glGetUniformLocation(self.program, b"texVolume"), 1)

        # draw front face of cubes
        self.raycube.renderFrontFace(pMatrix, mvMatrix, self.program)
                
        #self.render(pMatrix, mvMatrix)

    def keyPressed(self, key):
        if key == 'l':
            self.camera.rotate(True)
        elif key == 'r':
            self.camera.rotate(False)
            
    def reshape(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        self.raycube.reshape(width, height)

    def close(self):
        self.raycube.close()
