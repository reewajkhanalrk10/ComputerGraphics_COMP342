import pygame
from pygame.locals import *
from OpenGL.GL import *

def DDA_Line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))

    x_increment = dx / steps
    y_increment = dy / steps

    x = x1
    y = y1

    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

    for _ in range(steps):
        x += x_increment
        y += y_increment
        glBegin(GL_POINTS)
        glVertex2f(round(x), round(y))
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

        # Drawing the line using DDA algorithm
        DDA_Line(*point1, *point2)

        pygame.display.flip()

if __name__ == "__main__":
    main()
