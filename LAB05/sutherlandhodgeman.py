import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Define the clip region boundaries
LEFT = 0
RIGHT = 1
BOTTOM = 2
TOP = 3

# Function to check if a point is inside the clip boundary
def inside(point, boundary, value):
    if boundary == LEFT:
        return point[0] >= value
    elif boundary == RIGHT:
        return point[0] <= value
    elif boundary == BOTTOM:
        return point[1] >= value
    elif boundary == TOP:
        return point[1] <= value
    return False

# Function to compute the intersection point with the clip boundary
def intersect(point1, point2, boundary, value):
    if boundary == LEFT or boundary == RIGHT:
        x = value
        y = point1[1] + (point2[1] - point1[1]) * (value - point1[0]) / (point2[0] - point1[0])
    elif boundary == BOTTOM or boundary == TOP:
        y = value
        x = point1[0] + (point2[0] - point1[0]) * (value - point1[1]) / (point2[1] - point1[1])
    return [x, y]

# Sutherland-Hodgman polygon clipping algorithm
def sutherland_hodgman_clip(polygon, clip_window):
    clipped_polygon = polygon
    for boundary, value in clip_window.items():
        input_list = clipped_polygon
        clipped_polygon = []
        if not input_list:
            break
        s = input_list[-1]

        for e in input_list:
            if inside(e, boundary, value):
                if not inside(s, boundary, value):
                    clipped_polygon.append(intersect(s, e, boundary, value))
                clipped_polygon.append(e)
            elif inside(s, boundary, value):
                clipped_polygon.append(intersect(s, e, boundary, value))
            s = e

    return clipped_polygon

# Function to get user input for the clipping window
def get_window():
    print("Enter the clipping window coordinates (x_min, y_min, x_max, y_max):")
    x_min = int(input("x_min: "))
    y_min = int(input("y_min: "))
    x_max = int(input("x_max: "))
    y_max = int(input("y_max: "))
    return {LEFT: x_min, RIGHT: x_max, BOTTOM: y_min, TOP: y_max}

# Function to get user input for the polygon vertices
def get_polygon():
    print("Enter the number of vertices in the polygon:")
    num_vertices = int(input("Number of vertices: "))
    polygon = []
    for i in range(num_vertices):
        xy = input(f"Vertex {i+1} (x,y): ")
        x, y = map(int, xy.split(','))
        polygon.append([x, y])
    return polygon

def main():
    # Initialize Pygame and set up the OpenGL context
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glOrtho(0, 800, 0, 600, -1, 1)

    clip_window = get_window()

    running = True
    while running:
        # Get user input for the polygon vertices
        polygon = get_polygon()

        # Perform the clipping
        clipped_polygon = sutherland_hodgman_clip(polygon, clip_window)

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
            glVertex2f(clip_window[LEFT], clip_window[BOTTOM])
            glVertex2f(clip_window[RIGHT], clip_window[BOTTOM])
            glVertex2f(clip_window[RIGHT], clip_window[TOP])
            glVertex2f(clip_window[LEFT], clip_window[TOP])
            glEnd()

            # Draw the original polygon
            glColor3f(1, 0, 0)  # Red
            glBegin(GL_LINE_LOOP)
            for vertex in polygon:
                glVertex2f(vertex[0], vertex[1])
            glEnd()

            # Draw the clipped polygon if it exists
            if clipped_polygon:
                glColor3f(0, 0.5, 0)  # Dark Green
                glBegin(GL_LINE_LOOP)
                for vertex in clipped_polygon:
                    glVertex2f(vertex[0], vertex[1])
                glEnd()

            pygame.display.flip()
            pygame.time.wait(10)

        # Ask the user if they want to draw another polygon
        another_polygon = input("Draw another polygon? (y/n): ").strip().lower()
        if another_polygon != 'y':
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
