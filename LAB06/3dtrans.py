import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Cube vertices and edges
vertices = [
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

edges = [
    (0, 1, 2, 3),
    (3, 2, 6, 7),
    (7, 6, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 6, 2),
    (4, 0, 3, 7)
]

# Define colors for the cube faces (RGB)
colors = [
    (1, 0, 0),    # Red
    (0, 1, 0),    # Green
    (0, 0, 1),    # Blue
    (1, 1, 0),    # Yellow
    (1, 0, 1),    # Magenta
    (0, 1, 1)     # Cyan
]

# Transformation matrices
def translate(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def rotate_x(theta):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    return np.array([
        [1, 0, 0, 0],
        [0, cos_theta, -sin_theta, 0],
        [0, sin_theta, cos_theta, 0],
        [0, 0, 0, 1]
    ])

def rotate_y(theta):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    return np.array([
        [cos_theta, 0, sin_theta, 0],
        [0, 1, 0, 0],
        [-sin_theta, 0, cos_theta, 0],
        [0, 0, 0, 1]
    ])

def rotate_z(theta):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    return np.array([
        [cos_theta, -sin_theta, 0, 0],
        [sin_theta, cos_theta, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def scale(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def shear(shx, shy):
    return np.array([
        [1, shx, 0, 0],
        [shy, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def composite(*transformations):
    result = np.eye(4)
    for transformation in transformations:
        result = np.dot(transformation, result)
    return result

def draw_cube(vertices, transformed_vertices):
    glBegin(GL_QUADS)
    for i, (face, color) in enumerate(zip(edges, colors)):
        glColor3fv(color)
        for vertex in face:
            glVertex3fv(vertices[vertex])  # Use original vertices for drawing
    glEnd()

def display_menu():
    print("Choose an operation:")
    print("1. Translation")
    print("2. Rotation")
    print("3. Scaling")
    print("4. Shearing")
    print("5. Composite Transformation")
    print("6. Exit")

def get_input():
    while True:
        try:
            operation = int(input("Enter operation number: "))
            if operation in range(1, 7):
                break
            else:
                print("Invalid operation number. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input! Please enter a valid operation number.")
    
    if operation == 5:
        while True:
            try:
                print("Enter operations to be composed (e.g., '1 2 3' for translation, rotation, scaling):")
                operations = list(map(int, input().split()))
                if all(op in range(1, 5) for op in operations):
                    return operation, operations
                else:
                    print("Invalid operations. Please enter numbers between 1 and 4.")
            except ValueError:
                print("Invalid input! Please enter numbers separated by spaces.")
    
    return operation, None

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    transformed_vertices = np.eye(4)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        draw_cube(vertices, transformed_vertices)  # Draw original cube
        glPopMatrix()
        
        glPushMatrix()
        glMultMatrixf(transformed_vertices.T)
        draw_cube(vertices, transformed_vertices)  # Draw transformed cube
        glPopMatrix()
        
        pygame.display.flip()

        display_menu()
        operation, operations = get_input()

        if operation == 6:
            break
        else:
            transformation_matrix = None
            if operation == 1:
                tx, ty, tz = map(float, input("Enter translation values (tx,ty,tz): ").split(","))
                transformation_matrix = translate(tx, ty, tz)
            elif operation == 2:
                while True:
                    axis = input("Enter rotation axis (x, y, z): ").lower()
                    if axis in ['x', 'y', 'z']:
                        break
                    else:
                        print("Invalid axis. Please enter 'x', 'y', or 'z'.")
                theta = float(input("Enter rotation angle (in degrees): "))
                if axis == 'x':
                    transformation_matrix = rotate_x(np.radians(theta))
                elif axis == 'y':
                    transformation_matrix = rotate_y(np.radians(theta))
                elif axis == 'z':
                    transformation_matrix = rotate_z(np.radians(theta))
            elif operation == 3:
                sx, sy, sz = map(float, input("Enter scaling factors (sx,sy,sz): ").split(","))
                transformation_matrix = scale(sx, sy, sz)
            elif operation == 4:
                shx, shy = map(float, input("Enter shearing factors (shx,shy): ").split(","))
                transformation_matrix = shear(shx, shy)
            
            transformed_vertices = np.dot(transformation_matrix, transformed_vertices)

if __name__ == "__main__":
    main()
