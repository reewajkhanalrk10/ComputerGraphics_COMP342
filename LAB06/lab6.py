import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Initialize the library
if not glfw.init():
    raise Exception("GLFW can't be initialized")

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(800, 600, "3D Transformations", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

# Make the window's context current
glfw.make_context_current(window)

# Set up the projection matrix
glMatrixMode(GL_PROJECTION)
gluPerspective(45, 800 / 600, 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

def draw_cube():
    """Draws a 3D cube with different colors on each face."""
    glBegin(GL_QUADS)
    # Front face
    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    # Back face
    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    # Top face
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    # Bottom face
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    # Right face
    glColor3f(1.0, 0.0, 1.0)  # Magenta
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    # Left face
    glColor3f(0.0, 1.0, 1.0)  # Cyan
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glEnd()

def apply_transformations():
    """Applies transformations to the cube."""
    # Clear the screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Move back to see the object
    glTranslatef(0.0, 0.0, -5)

    # Apply transformations
    glTranslatef(*translation_params)  # Translation
    glRotatef(*rotation_params)       # Rotation
    glScalef(*scaling_params)         # Scaling
    glMultMatrixf(shearing_matrix)    # Shearing

    # Draw the cube
    draw_cube()

    # Swap front and back buffers
    glfw.swap_buffers(window)

def get_user_input():
    """Prompts the user for transformation parameters."""
    global translation_params, rotation_params, scaling_params, shearing_matrix

    # For testing purposes, set default values
    translation_params = (1.0, 1.0, 0.0)
    rotation_params = (45.0, 1.0, 1.0, 0.0)
    scaling_params = (0.5, 0.5, 0.5)
    shearing_matrix = np.array([
        [1, 0.5, 0, 0],
        [0.5, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    # Ask the user for translation parameters
    print("Enter translation parameters (x, y, z):")
    try:
        translation_params = tuple(map(float, input().split()))
    except ValueError:
        print("Invalid input. Using default translation parameters.")

    # Ask the user for rotation parameters
    print("Enter rotation parameters (angle, x, y, z):")
    try:
        rotation_params = tuple(map(float, input().split()))
    except ValueError:
        print("Invalid input. Using default rotation parameters.")

    # Ask the user for scaling parameters
    print("Enter scaling parameters (x, y, z):")
    try:
        scaling_params = tuple(map(float, input().split()))
    except ValueError:
        print("Invalid input. Using default scaling parameters.")

    # Ask the user for shearing matrix
    print("Enter shearing matrix (4x4) row-wise:")
    try:
        shearing_matrix = np.array([list(map(float, input().split())) for _ in range(4)], dtype=np.float32)
    except ValueError:
        print("Invalid input. Using default shearing matrix.")

# Initialize transformation parameters
translation_params = (0.0, 0.0, 0.0)
rotation_params = (0.0, 0.0, 0.0, 0.0)
scaling_params = (1.0, 1.0, 1.0)
shearing_matrix = np.identity(4, dtype=np.float32)

# Get user input for transformation parameters
get_user_input()

# Loop until the user closes the window
while not glfw.window_should_close(window):
    # Apply transformations and draw the cube
    apply_transformations()

    # Poll for and process events
    glfw.poll_events()

# Terminate GLFW
glfw.terminate()
