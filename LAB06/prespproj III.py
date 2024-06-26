import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

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

def draw_projection_plane():
    """Draws a projection plane."""
    glColor3fv((1, 1, 1))  # White
    glBegin(GL_QUADS)
    glVertex3f(-2, -2, -5)
    glVertex3f(2, -2, -5)
    glVertex3f(2, 2, -5)
    glVertex3f(-2, 2, -5)
    glEnd()

def project_vertices(vertices, projection_matrix):
    """Projects vertices onto the projection plane."""
    projected_vertices = []
    for vertex in vertices:
        vertex_4d = np.append(vertex, 1)  # Convert to 4D
        projected_vertex = np.dot(projection_matrix, vertex_4d)  # Apply projection
        projected_vertex /= projected_vertex[-1]  # Normalize
        projected_vertices.append(projected_vertex[:-1])  # Convert back to 3D
    return projected_vertices

def perspective_projection(fov):
    """Sets up a perspective projection matrix with a given field of view (FOV)."""
    glMatrixMode(GL_PROJECTION)  # Select the projection matrix
    glLoadIdentity()  # Reset the projection matrix
    gluPerspective(fov, (800 / 600), 0.1, 50.0)  # Set up a perspective projection
    glMatrixMode(GL_MODELVIEW)  # Select the modelview matrix
    glLoadIdentity()  # Reset the modelview matrix

def main():
    """Main function to initialize and run the OpenGL/pygame window."""
    pygame.init()  # Initialize pygame
    display = (800, 600)  # Set the display size
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # Set the display mode to double buffer and OpenGL

    # Initialize rotation, scaling, shearing, and field of view variables
    rotation_x, rotation_y = 0, 0
    scale = 1.0
    shear = 0.0
    fov = 45

    perspective_projection(fov)  # Apply the perspective projection
    glTranslatef(0, 0, -5)  # Translate the scene

    while True:
        for event in pygame.event.get():  # Event handling
            if event.type == pygame.QUIT:  # Exit condition
                pygame.quit()  # Quit pygame
                quit()  # Exit the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Rotate left
                    rotation_y -= 5
                if event.key == pygame.K_RIGHT:  # Rotate right
                    rotation_y += 5
                if event.key == pygame.K_UP:  # Rotate up
                    rotation_x -= 5
                if event.key == pygame.K_DOWN:  # Rotate down
                    rotation_x += 5
                if event.key == pygame.K_a:  # Decrease FOV
                    fov -= 5
                    if fov < 10:
                        fov = 10
                    perspective_projection(fov)
                if event.key == pygame.K_d:  # Increase FOV
                    fov += 5
                    if fov > 120:
                        fov = 120
                    perspective_projection(fov)
                if event.key == pygame.K_s:  # Scale down
                    scale -= 0.1
                    if scale < 0.1:
                        scale = 0.1
                if event.key == pygame.K_w:  # Scale up
                    scale += 0.1
                if event.key == pygame.K_q:  # Shear left
                    shear -= 0.1
                if event.key == pygame.K_e:  # Shear right
                    shear += 0.1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen and depth buffer

        glPushMatrix()  # Save the current matrix

        # Apply scaling
        glScalef(scale, scale, scale)

        # Apply shearing
        shear_matrix = np.array([
            [1, shear, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        glMultMatrixf(shear_matrix.T)

        # Apply rotation
        glRotatef(rotation_x, 1, 0, 0)  # Apply rotation around the x-axis
        glRotatef(rotation_y, 0, 1, 0)  # Apply rotation around the y-axis

        draw_cuboid()  # Draw the cuboid
        glPopMatrix()  # Restore the previous matrix

        # Draw the projection plane
        draw_projection_plane()

        pygame.display.flip()  # Swap the buffers
        pygame.time.wait(10)  # Wait for 10 milliseconds

main()
