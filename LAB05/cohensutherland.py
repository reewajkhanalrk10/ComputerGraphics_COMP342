import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Constants for region codes
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

# Function to compute the region code for a point (x, y)
def compute_outcode(x, y, x_min, y_min, x_max, y_max):
    code = INSIDE

    if x < x_min:      # to the left of the rectangle
        code |= LEFT
    elif x > x_max:    # to the right of the rectangle
        code |= RIGHT
    if y < y_min:      # below the rectangle
        code |= BOTTOM
    elif y > y_max:    # above the rectangle
        code |= TOP

    return code

# Function to implement Cohen-Sutherland line clipping algorithm
def cohen_sutherland_clip(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    # Compute the outcodes for the two endpoints
    outcode1 = compute_outcode(x1, y1, x_min, y_min, x_max, y_max)
    outcode2 = compute_outcode(x2, y2, x_min, y_min, x_max, y_max)
    accept = False

    while True:
        if outcode1 == 0 and outcode2 == 0:
            # Both endpoints lie inside the rectangle
            accept = True
            break
        elif outcode1 & outcode2 != 0:
            # Both endpoints share an outside zone (trivial reject)
            break
        else:
            # Some segment of the line lies within the rectangle
            x, y = 0, 0

            # At least one endpoint is outside the rectangle, select it
            outcode_out = outcode1 if outcode1 != 0 else outcode2

            # Find the intersection point using the outcode
            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            # Replace the endpoint outside the rectangle with the intersection point
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1, x_min, y_min, x_max, y_max)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2, x_min, y_min, x_max, y_max)

    if accept:
        return (x1, y1, x2, y2)
    else:
        return None

# Function to get user input for the clipping window
def get_window():
    print("Enter the clipping window coordinates (x_min, y_min, x_max, y_max):")
    x_min = int(input("x_min: "))
    y_min = int(input("y_min: "))
    x_max = int(input("x_max: "))
    y_max = int(input("y_max: "))
    return x_min, y_min, x_max, y_max

# Function to get user input for the line segment
def get_line():
    xy1 = input("Input x1,y1: ")
    x1, y1 = map(int, xy1.split(','))
    xy2 = input("Input x2,y2: ")
    x2, y2 = map(int, xy2.split(','))
    return x1, y1, x2, y2

def main():
    # Initialize Pygame and set up the OpenGL context
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glOrtho(0, 800, 0, 600, -1, 1)

    x_min, y_min, x_max, y_max = get_window()

    running = True
    while running:
        # Get user input for the line segment
        x1, y1, x2, y2 = get_line()

        # Perform the clipping
        clipped_line = cohen_sutherland_clip(x1, y1, x2, y2, x_min, y_min, x_max, y_max)

        drawing = True
        while drawing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    drawing = False

            glClearColor(1.0, 1.0, 1.0, 1.0)  # Set background color to white
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Draw the clipping window
            glColor3f(0, 0, 0)  # Black
            glBegin(GL_LINE_LOOP)
            glVertex2f(x_min, y_min)
            glVertex2f(x_max, y_min)
            glVertex2f(x_max, y_max)
            glVertex2f(x_min, y_max)
            glEnd()

            # Draw the original line segment
            glColor3f(1, 0, 0)  # Red
            glBegin(GL_LINES)
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
            glEnd()

            # Draw the clipped line segment if it exists
            if clipped_line:
                glColor3f(0, 0.5, 0)  # Dark Green
                glBegin(GL_LINES)
                glVertex2f(clipped_line[0], clipped_line[1])
                glVertex2f(clipped_line[2], clipped_line[3])
                glEnd()

            pygame.display.flip()
            pygame.time.wait(10)

        # Ask the user if they want to draw another line
        another_line = input("Draw another line? (y/n): ").strip().lower()
        if another_line != 'y':
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
