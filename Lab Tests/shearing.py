import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Cube vertices
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Cube edges
edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7]
]

# Shearing factors
shearing_factors = [0.0, 0.0, 0.0]

# Scaling factor for the cube
scaling_factor = 0.25  # Adjust the scaling factor here

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv([v * scaling_factor for v in vertices[vertex]])  # Scale each vertex
    glEnd()

def apply_shearing(axis):
    shearing_matrix = np.identity(4, dtype=np.float32)
    if axis == 'x':
        shearing_matrix[1, 0] = shearing_factors[0]  # Shearing only along the x-axis
    elif axis == 'y':
        shearing_matrix[2, 1] = shearing_factors[0]  # Shearing only along the y-axis
    elif axis == 'z':
        shearing_matrix[3, 2] = shearing_factors[0]  # Shearing only along the z-axis
    glMultMatrixf(shearing_matrix)
    glColor3f(1.0, 1.0, 0.0)  # Original cube color
    draw_cube()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)  # Camera position

    glColor3f(1.0, 1.0, 1.0)
    draw_cube()

    # Draw axes
    glLineWidth(2.0)
    glBegin(GL_LINES)
    # x-axis (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-2.0, 0.0, 0.0)
    glVertex3f(2.0, 0.0, 0.0)
    # y-axis (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -2.0, 0.0)
    glVertex3f(0.0, 2.0, 0.0)
    # z-axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -2.0)
    glVertex3f(0.0, 0.0, 2.0)
    glEnd()

    # Draw origin
    glPointSize(5.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glEnd()

    apply_shearing('y')  # Change the axis here

    glFlush()

def key_callback(window, key, scancode, action, mods):
    global shearing_factors
    if key == glfw.KEY_LEFT and action == glfw.PRESS:
        shearing_factors[0] -= 0.1
    elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
        shearing_factors[0] += 0.1

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "3D Shearing ", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        display()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
