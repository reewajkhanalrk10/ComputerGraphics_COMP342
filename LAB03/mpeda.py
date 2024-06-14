import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Function to plot points in all four quadrants
def plot_ellipse_points(x_center, y_center, x, y):
    glBegin(GL_POINTS)
    # Quadrant: 1 Right Top
    glVertex2i(x_center + x, y_center + y)
    # Quadrant: 2 Right Bottom
    glVertex2i(x_center + x, y_center - y)
    #Quadrant: 3 Left Bottom
    glVertex2i(x_center - x, y_center - y)
    # Quadrant: 4 Left Top
    glVertex2i(x_center - x, y_center + y)
    glEnd()

# Mid-Point Ellipse Drawing Algorithm
def midpoint_ellipse(x_center, y_center, rx, ry):
    x = 0
    y = ry
    rx2 = rx * rx
    ry2 = ry * ry
    tworx2 = 2 * rx2
    twory2 = 2 * ry2
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)  # Decision parameter for region 1
    dx = twory2 * x
    dy = tworx2 * y

    # Region 1
    while dx < dy:
        plot_ellipse_points(x_center, y_center, x, y)
        if p1 < 0:
            x += 1
            dx += twory2
            p1 += dx + ry2
        else:
            x += 1
            y -= 1
            dx += twory2
            dy -= tworx2
            p1 += dx - dy + ry2

    # Region 2
    # Decision Parameter for region 2
    p2 = (ry2 * (x + 0.5) * (x + 0.5)) + (rx2 * (y - 1) * (y - 1)) - (rx2 * ry2)
    while y >= 0:
        plot_ellipse_points(x_center, y_center, x, y)
        if p2 > 0:
            y -= 1
            dy -= tworx2
            p2 += rx2 - dy
        else:
            x += 1
            y -= 1
            dx += twory2
            dy -= tworx2
            p2 += dx - dy + rx2

def draw_axes():
    glBegin(GL_LINES)
    # Draw X axis
    glVertex2i(-400, 0)
    glVertex2i(400, 0)
    # Draw Y axis
    glVertex2i(0, -300)
    glVertex2i(0, 300)
    glEnd()

def draw_ellipse(x_center=0,y_center=0,rx=100,ry=50):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    # Draw the axes
    draw_axes()
    
    # Draw the ellipse
    midpoint_ellipse(x_center, y_center, rx, ry)  # Draw ellipse
    glFlush()

def get_input():
    x_center = int(input("Enter x coordinate of origin: "))
    y_center = int(input("Enter y coordinate of origin: "))
    rx = int(input("Enter x radius of ellipse: "))
    ry = int(input("Enter y radius of ellipse: "))
    return x_center, y_center, rx, ry

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(-400, 400, -300, 300)  # Set up 2D coordinate system
    # x_center,y_center,rx,ry=get_input()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_ellipse(x_center=0,y_center=0,rx=100,ry=200)
        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()
