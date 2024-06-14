import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def plot_circle_points(x_center, y_center, points):
    glBegin(GL_LINE_LOOP)
    for x, y in points:
        glVertex2i(x_center + x, y_center + y)
    glEnd()

def polar_circle(x_center, y_center, radius):
    points = []
    theta = 0
    step = 0.01  # Small step for smooth circle

    while theta <= 2 * math.pi:
        x = int(radius * math.cos(theta))
        y = int(radius * math.sin(theta))
        points.append((x, y))
        theta += step
    
    plot_circle_points(x_center, y_center, points)

def draw_axes():
    glBegin(GL_LINES)
    # Draw X axis
    glVertex2i(-400, 0)
    glVertex2i(400, 0)
    # Draw Y axis
    glVertex2i(0, -300)
    glVertex2i(0, 300)
    glEnd()

def draw_circle(x_center, y_center, radius):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    draw_axes()
    polar_circle(x_center, y_center, radius)
    glFlush()

def get_input():
    x_center = int(input("Enter x coordinate of origin: "))
    y_center = int(input("Enter y coordinate of origin: "))
    radius = int(input("Enter radius of circle: "))
    return x_center, y_center, radius

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(-400, 400, -300, 300)  # Set up 2D coordinate system
    # x_center, y_center, radius = get_input()
    x_center,y_center,radius= 100,100,100
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_circle(x_center, y_center, radius)
        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()