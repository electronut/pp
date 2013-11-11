"""
simplegl.py

Simple Python OpenGL program that uses shaders and a texture.

Author: Mahesh Venkitachalam
"""

import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *

import numpy, math, sys 
import glutils

strVS = """
attribute vec3 aVert;
uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform vec4 uColor;

varying vec4 vCol;
varying vec2 vTexCoord;

uniform float uTheta;

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
varying vec4 vCol;
uniform sampler2D tex2D;
varying vec2 vTexCoord;
uniform bool showCircle;

void main() {
  if (showCircle) {
    // discard fragment outside circle
    if (distance(vTexCoord, vec2(0.5, 0.5)) > 0.5) {
      discard;
    }
    else {
      gl_FragColor = texture2D(tex2D, vTexCoord);
    }
  }
  else {
     gl_FragColor = texture2D(tex2D, vTexCoord);
  }
}

"""

# 3D scene
class Scene:
    
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

        # attributes
        self.vertIndex = glGetAttribLocation(self.program, "aVert")

        # color
        self.col0 = [1.0, 0.0, 0.0, 1.0]

        # texture 
        self.tex2D = glGetUniformLocation(self.program, "tex2D")

        # define quad vertices 
        quadV = [
            -0.5, -0.5, 0.0, 
            0.5, -0.5, 0.0, 
            0.5, 0.5, 0.0,
            -0.5, 0.5, 0.0
            ]

        # vertices
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        vertexData = numpy.array(quadV, numpy.float32)
        glBufferData(GL_ARRAY_BUFFER, 4*len(vertexData), vertexData, 
                     GL_STATIC_DRAW)
        # time
        self.t = 0 

        # texture
        self.texId = glutils.loadTexture('test.png')

        # show circle?
        self.showCircle = False

    # step
    def step(self):
        # increment angle
        self.t = (self.t + 5) % 360
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

        # set color
        glUniform4fv(self.colorU, 1, self.col0)

        #enable arrays
        glEnableVertexAttribArray(self.vertIndex)

        # set buffers 
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, 0, None)

        # texture 
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texId)
        glEnable(GL_TEXTURE_2D)
        glUniform1i(self.tex2D, 0)

        # draw
        glDrawArrays(GL_QUADS, 0, 4)
        
        glDisable(GL_TEXTURE_2D)

        # disable arrays
        glDisableVertexAttribArray(self.vertIndex)            
        

class RenderWindow:
    def __init__(self, argv):
        glutInit(argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
        glutInitWindowSize(400, 400)
        self.window = glutCreateWindow("Simple GL")
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.draw)
        glutKeyboardFunc(self.keyPressed) # Checks for key strokes
        glutTimerFunc(100, self.update, 0)
        self.scene = Scene()
        glutMainLoop()

    def reshape(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.5, 0.5,1.0)
        glutPostRedisplay()

    def keyPressed(self, *args):
        if args[0] == '\x1b':
            sys.exit()
        else:
            self.scene.showCircle = not self.scene.showCircle
            glUniform1i(glGetUniformLocation(self.scene.program, 'showCircle'), 
                        self.scene.showCircle)
            glutPostRedisplay()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # build projection matrix
        pMatrix = glutils.perspective(45.0, self.aspect, 0.1, 100.0)
       
        mvMatrix = glutils.lookAt([0.0, 0.0, -2.0], [0.0, 0.0, 0.0],
                                  [0.0, 1.0, 0.0])
        # render
        self.scene.render(pMatrix, mvMatrix)
        # swap buffers
        glutSwapBuffers()

    def update(self, *args):
        self.scene.step();
        glutPostRedisplay()
        glutTimerFunc(100, self.update, 0)

# main() function
def main():
    prog = RenderWindow(sys.argv)

# call main
if __name__ == '__main__':
    main()
