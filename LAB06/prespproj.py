import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Define the vertices of the cuboid
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

# Define the edges of the cuboid
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Define the faces of the cuboid
faces = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
    (0, 3, 7, 4),
    (1, 2, 6, 5)
]

# Define colors for each face
colors = [
    (1, 0, 0),  # Red
    (0, 1, 0),  # Green
    (0, 0, 1),  # Blue
    (1, 1, 0),  # Yellow
    (1, 0, 1),  # Magenta
    (0, 1, 1)   # Cyan
]

def draw_cuboid():
    """Draws a cuboid with colored faces."""
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        glBegin(GL_QUADS)
        for vertex in face:
            glVertex3fv(vertices[vertex])
        glEnd()

def perspective_projection():
    """Sets up a perspective projection matrix."""
    glMatrixMode(GL_PROJECTION)  # Select the projection matrix
    glLoadIdentity()  # Reset the projection matrix
    gluPerspective(45, (800/600), 0.1, 50.0)  # Set up a perspective projection
    glMatrixMode(GL_MODELVIEW)  # Select the modelview matrix
    glLoadIdentity()  # Reset the modelview matrix

def main():
    """Main function to initialize and run the OpenGL/pygame window."""
    pygame.init()  # Initialize pygame
    display = (800, 600)  # Set the display size
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # Set the display mode to double buffer and OpenGL
    perspective_projection()  # Apply the perspective projection
    glTranslatef(0, 0, -5)  # Translate the scene

    while True:
        for event in pygame.event.get():  # Event handling
            if event.type == pygame.QUIT:  # Exit condition
                pygame.quit()  # Quit pygame
                quit()  # Exit the program

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen and depth buffer
        draw_cuboid()  # Draw the cuboid
        pygame.display.flip()  # Swap the buffers
        pygame.time.wait(10)  # Wait for 10 milliseconds

main()
