import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Function to plot points in all octants
def plot_circle_points(x_center, y_center, x, y):
    glBegin(GL_POINTS)
    # Reflecting the points in all octants
    # Octant 1: Right Top Up
    glVertex2i(x_center + y, y_center + x)
    # Octant 2: Right Top
    glVertex2i(x_center + x, y_center + y)
    # Octant 3: Right Bottom Up
    glVertex2i(x_center + y, y_center - x)
    # Octant 4: Right Bottom
    glVertex2i(x_center + x, y_center - y)
    # Octant 5: Left Bottom
    glVertex2i(x_center - x, y_center - y)
    # Octant 6: Left Bottom Up
    glVertex2i(x_center - y, y_center - x)
    # Octant 7: Left Top Up
    glVertex2i(x_center - y, y_center + x)
    # Octant 8: Left Top
    glVertex2i(x_center - x, y_center + y)
    glEnd()

# Mid-Point Circle Drawing Algorithm
def midpoint_circle(x_center, y_center, radius):
    x = 0
    y = radius
    d = 1 - radius  # Decision parameter
    plot_circle_points(x_center, y_center, x, y)
    
    while x < y:
        if d < 0:
            # Move to the right
            d = d + 2 * x + 3
        else:
            # Move to the right and down
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        plot_circle_points(x_center, y_center, x, y)

def draw_circle(x_center,y_center,radius):
    
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    # Draw the axes
    draw_axes()
    midpoint_circle(x_center, y_center, radius)  # Draw circle with radius 100 at origin
    glFlush()

def draw_axes():
    glBegin(GL_LINES)
    # Draw X axis
    glVertex2i(-400, 0)
    glVertex2i(400, 0)
    # Draw Y axis
    glVertex2i(0, -300)
    glVertex2i(0, 300)
    glEnd()


def get_input():
    x_center=int(input("Enter x coordinate of origin"))
    y_center=int(input("Enter x coordinate of origin"))
    radius=int(input("Enter radius of circle"))
    return x_center,y_center,radius

    
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(-400, 400, -300, 300)  # Set up 2D coordinate system
    # x_center,y_center,radius=get_input()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_circle(x_center=50,y_center=50,radius=100)
        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()
