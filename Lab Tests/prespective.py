import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Initialize the library
if not glfw.init():
    raise Exception("GLFW can't be initialized")

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(800, 600, "3D Transformations with Perspective Projection", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

# Make the window's context current
glfw.make_context_current(window)

# Set up the projection matrix with a different FOV to demonstrate perspective projection
def setup_perspective(fov):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, 800 / 600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

def draw_cube():
    glBegin(GL_QUADS)
    # Front face
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    # Back face
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    # Top face
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    # Bottom face
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    # Right face
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    # Left face
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glEnd()

def apply_transformations():
    # Clear the screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Move back to see the object
    glTranslatef(0.0, 0.0, -5)

    # Apply transformations
    glTranslatef(1.0, 1.0, 0.0)  # Translation
    glRotatef(45, 1, 1, 0)       # Rotation
    glScalef(0.5, 0.5, 0.5)      # Scaling to make the object smaller
    shear_matrix = np.array([
        [1, 0.5, 0, 0],
        [0.5, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)
    glMultMatrixf(shear_matrix)  # Shearing

    # Draw the cube
    draw_cube()

    # Swap front and back buffers
    glfw.swap_buffers(window)

# Loop until the user closes the window
while not glfw.window_should_close(window):
    # Apply transformations and draw the cube
    setup_perspective(90)  # Change FOV to 30 degrees
    apply_transformations()

    # Poll for and process events
    glfw.poll_events()

# Terminate GLFW
glfw.terminate()
