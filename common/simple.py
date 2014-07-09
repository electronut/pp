# -----------------------------------------------------------------------------
#  GLFW - An OpenGL framework
#  API version: 3.0.1
#  WWW:         http://www.glfw.org/
#  ----------------------------------------------------------------------------
#  Copyright (c) 2002-2006 Marcus Geelnard
#  Copyright (c) 2006-2010 Camilla Berglund
#
#  Python bindings - Copyright (c) 2013 Nicolas P. Rougier
#
#  This software is provided 'as-is', without any express or implied
#  warranty. In no event will the authors be held liable for any damages
#  arising from the use of this software.
#
#  Permission is granted to anyone to use this software for any purpose,
#  including commercial applications, and to alter it and redistribute it
#  freely, subject to the following restrictions:
#
#  1. The origin of this software must not be misrepresented; you must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would
#     be appreciated but is not required.
#
#  2. Altered source versions must be plainly marked as such, and must not
#     be misrepresented as being the original software.
#
#  3. This notice may not be removed or altered from any source
#     distribution.
#
# -----------------------------------------------------------------------------
#
# This short example shows how the GLFW API looks and how easy it is to create
# and a window and OpenGL context with it. There are many more functions than
# those used here, but these are all you need to get started.
#
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    import glfw
    import OpenGL.GL as gl

    def on_key(window, key, scancode, action, mods):
        if key == glfw.GLFW_KEY_ESCAPE and action == glfw.GLFW_PRESS:
            glfw.glfwSetWindowShouldClose(window,1)

    # Initialize the library
    if not glfw.glfwInit():
        sys.exit()

    # Create a windowed mode window and its OpenGL context
    window = glfw.glfwCreateWindow(640, 480, "Hello World", None, None)
    if not window:
        glfw.glfwTerminate()
        sys.exit()

    # Make the window's context current
    glfw.glfwMakeContextCurrent(window)

    # Install a key handler
    glfw.glfwSetKeyCallback(window, on_key)

    # Loop until the user closes the window
    while not glfw.glfwWindowShouldClose(window):
        # Render here
        width, height = glfw.glfwGetFramebufferSize(window)
        ratio = width / float(height)
        gl.glViewport(0, 0, width, height)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-ratio, ratio, -1, 1, 1, -1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        # gl.glRotatef(glfw.glfwGetTime() * 50, 0, 0, 1)
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glColor3f(1, 0, 0)
        gl.glVertex3f(-0.6, -0.4, 0)
        gl.glColor3f(0, 1, 0)
        gl.glVertex3f(0.6, -0.4, 0)
        gl.glColor3f(0, 0, 1)
        gl.glVertex3f(0, 0.6, 0)
        gl.glEnd()

        # Swap front and back buffers
        glfw.glfwSwapBuffers(window)

        # Poll for and process events
        glfw.glfwPollEvents()

    glfw.glfwTerminate()
