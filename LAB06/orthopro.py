import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Define the vertices of the tetrahedron
vertices = [
    [0, 1, 0],
    [-1, -1, 1],
    [1, -1, 1],
    [0, -1, -1]
]

# Define the faces of the tetrahedron
faces = [
    (0, 1, 2),
    (0, 1, 3),
    (0, 2, 3),
    (1, 2, 3)
]

# Define colors for each face
colors = [
    (1, 0, 0),  # Red
    (0, 1, 0),  # Green
    (0, 0, 1),  # Blue
    (1, 1, 0)   # Yellow
]

def draw_tetrahedron():
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        glBegin(GL_TRIANGLES)
        for vertex in face:
            glVertex3fv(vertices[vertex])
        glEnd()

def ortho_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, -2, 2)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        ortho_projection()
        draw_tetrahedron()
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

main()
