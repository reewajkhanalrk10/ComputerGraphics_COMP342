import pygame
from pygame.locals import *
from OpenGL.GL import *

def Bresenham_Line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    slope_error = dx - dy

    x, y = x1, y1

    x_increment = 1 if x2 > x1 else -1
    y_increment = 1 if y2 > y1 else -1

    glBegin(GL_POINTS)
    glVertex2f(x, y)

    if dx > dy:  # |m| < 1
        slope_double_error = slope_error * 2
        while x != x2:
            x += x_increment
            if slope_error >= 0:
                y += y_increment
                slope_error -= slope_double_error
            slope_error += dx * 2
            glVertex2f(x, y)
    else:  # |m| >= 1
        slope_double_error = slope_error * 2
        while y != y2:
            y += y_increment
            if slope_error >= 0:
                x += x_increment
                slope_error -= slope_double_error
            slope_error += dy * 2
            glVertex2f(x, y)
    
    glEnd()

def get_point():
    x = int(input("Enter x coordinate: "))
    y = int(input("Enter y coordinate: "))
    return x, y

def main():
    # Prompt user for coordinates of two points
    print("Enter coordinates for the first point:")
    point1 = get_point()
    print("Enter coordinates for the second point:")
    point2 = get_point()

    # Determine screen dimensions based on input points
    max_x = max(point1[0], point2[0])
    max_y = max(point1[1], point2[1])
    screen_width = max_x + 100  # Add padding
    screen_height = max_y + 100  # Add padding

    pygame.init()
    display = (screen_width, screen_height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glOrtho(0, screen_width, 0, screen_height, -1, 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor3f(1, 1, 1)  # Set line color to white

        # Drawing the line using Bresenham algorithm
        Bresenham_Line(*point1, *point2)

        pygame.display.flip()

if __name__ == "__main__":
    main()
