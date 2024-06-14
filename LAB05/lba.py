import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def liang_barsky(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    """
    Liang-Barsky line clipping algorithm.

    Parameters:
    x0, y0: float, float
        Starting coordinates of the line.
    x1, y1: float, float
        Ending coordinates of the line.
    xmin, ymin, xmax, ymax: float, float, float, float
        Coordinates of the clipping window.

    Returns:
    clipped_line: tuple
        Clipped line coordinates (x0, y0, x1, y1) or None if the line is outside the window.
    """
    def clip(p, q, t0, t1):
        """
        Helper function to perform clipping against one boundary.

        Parameters:
        p: float
            The delta value for the current boundary.
        q: float
            The distance to the boundary.
        t0: float
            The lower bound parameter.
        t1: float
            The upper bound parameter.

        Returns:
        result: bool
            Whether the line is within the boundary.
        t0: float
            Updated lower bound parameter.
        t1: float
            Updated upper bound parameter.
        """
        if p < 0.0:
            r = q / p
            if r > t1:
                return False, t0, t1
            elif r > t0:
                t0 = r
        elif p > 0.0:
            r = q / p
            if r < t0:
                return False, t0, t1
            elif r < t1:
                t1 = r
        elif q < 0.0:
            return False, t0, t1
        return True, t0, t1

    # Calculate the differences
    dx = x1 - x0
    dy = y1 - y0

    # Coefficients and constants for inequalities
    p = [-dx, dx, -dy, dy]
    q = [x0 - xmin, xmax - x0, y0 - ymin, ymax - y0]

    # Initialize parameters
    t0, t1 = 0.0, 1.0

    # Process each boundary
    for i in range(4):
        result, t0, t1 = clip(p[i], q[i], t0, t1)
        if not result:
            return None  # Line is outside the clipping window

    # Calculate the clipped coordinates
    x0_clipped = x0 + t0 * dx
    y0_clipped = y0 + t0 * dy
    x1_clipped = x0 + t1 * dx
    y1_clipped = y0 + t1 * dy

    return x0_clipped, y0_clipped, x1_clipped, y1_clipped

def draw_line(x0, y0, x1, y1):
    """
    Draw a line using OpenGL.

    Parameters:
    x0, y0: float, float
        Starting coordinates of the line.
    x1, y1: float, float
        Ending coordinates of the line.
    """
    glBegin(GL_LINES)
    glVertex2f(x0, y0)
    glVertex2f(x1, y1)
    glEnd()

def main():
    # Get user input for the screen resolution
    screen_width = int(input("Enter the screen width: "))
    screen_height = int(input("Enter the screen height: "))

    # Print the screen resolution
    print(f"Screen resolution: {screen_width}x{screen_height}")

    # Get user input for the line coordinates
    x0 = float(input("Enter the x-coordinate of the starting point: "))
    y0 = float(input("Enter the y-coordinate of the starting point: "))
    x1 = float(input("Enter the x-coordinate of the ending point: "))
    y1 = float(input("Enter the y-coordinate of the ending point: "))

    # Get user input for the clipping window coordinates
    xmin = float(input("Enter the x-coordinate of the minimum clipping window: "))
    ymin = float(input("Enter the y-coordinate of the minimum clipping window: "))
    xmax = float(input("Enter the x-coordinate of the maximum clipping window: "))
    ymax = float(input("Enter the y-coordinate of the maximum clipping window: "))

    # Perform the clipping
    clipped_line = liang_barsky(x0, y0, x1, y1, xmin, ymin, xmax, ymax)

    # Initialize Pygame and set up the OpenGL display
    pygame.init()
    display = (screen_width, screen_height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(0, screen_width, 0, screen_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the clipping window
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(xmin, ymin)
        glVertex2f(xmax, ymin)
        glVertex2f(xmax, ymax)
        glVertex2f(xmin, ymax)
        glEnd()

        # Draw the original line
        glColor3f(0.0, 1.0, 0.0)
        draw_line(x0, y0, x1, y1)

        # Draw the clipped line
        if clipped_line:
            glColor3f(0.0, 0.0, 1.0)
            draw_line(*clipped_line)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
