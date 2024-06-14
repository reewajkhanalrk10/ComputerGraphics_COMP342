import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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

# Translation vector
translation = [0.0, 0.0, 0.0]

# Scaling factor for the cube
scaling_factor = 0.25  # Adjust the scaling factor here

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv([v * scaling_factor for v in vertices[vertex]])  # Scale each vertex
    glEnd()

def draw_axes():
    glLineWidth(2.0)
    glBegin(GL_LINES)
    # x-axis (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    # y-axis (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    # z-axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -1.0)
    glVertex3f(0.0, 0.0, 1.0)
    glEnd()

def apply_translation():
    glPushMatrix()
    glTranslatef(translation[0], translation[1], translation[2])
    glColor3f(1.0, 0.0, 0.0)  # Original cube color
    draw_cube()
    glPopMatrix()

def apply_scaling():
    # Find the front vertex
    front_vertex = vertices[2]  # Assuming the front vertex is the third vertex

    glPushMatrix()
    glTranslatef(front_vertex[0], front_vertex[1], front_vertex[2])  # Translate to the front vertex
    glScalef(2.5, 2.5, 2.5)  # Scale the cube
    glTranslatef(-front_vertex[0], -front_vertex[1], -front_vertex[2])  # Translate back
    glColor3f(0.0, 1.0, 0.0)  # Scaled cube color
    draw_cube()
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)  # Camera position

    glColor3f(1.0, 1.0, 1.0)
    draw_cube()
    draw_axes()  # Draw axes at the origin
    # apply_translation()
    apply_scaling()
   

    glFlush()
    
def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "3D Transformations", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

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
