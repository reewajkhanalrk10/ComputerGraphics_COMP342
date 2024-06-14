import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Cube vertices
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Cube edges
edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7]
]

# Transformation parameters
translation = [0.0, 0.0, 0.0]
scaling_factor = 1.0
rotation_axis = [1, 0, 0]
rotation_angle = 0
shearing_factors = [0.0, 0.0, 0.0]
current_transformation = None

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv([v * scaling_factor for v in vertices[vertex]])  # Scale each vertex
    glEnd()

def apply_translation():
    glPushMatrix()
    glTranslatef(translation[0], translation[1], translation[2])
    draw_cube()
    glPopMatrix()

def apply_scaling():
    glPushMatrix()
    glScalef(scaling_factor, scaling_factor, scaling_factor)
    draw_cube()
    glPopMatrix()

def apply_rotation():
    global rotation_axis, rotation_angle
    glPushMatrix()
    glRotatef(rotation_angle, *rotation_axis)
    draw_cube()
    glPopMatrix()

def apply_shearing(axis):
    shearing_matrix = np.identity(4, dtype=np.float32)
    if axis == 'x':
        shearing_matrix[1, 0] = shearing_factors[0]  # Shearing only along the x-axis
    elif axis == 'y':
        shearing_matrix[2, 1] = shearing_factors[0]  # Shearing only along the y-axis
    elif axis == 'z':
        shearing_matrix[3, 2] = shearing_factors[0]  # Shearing only along the z-axis
    glMultMatrixf(shearing_matrix)
    draw_cube()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)  # Camera position

    if current_transformation == 'translation':
        apply_translation()
    elif current_transformation == 'scaling':
        apply_scaling()
    elif current_transformation == 'rotation':
        apply_rotation()
    elif current_transformation == 'shearing':
        apply_shearing('y')  # Change the axis here

    glFlush()

def key_callback(window, key, scancode, action, mods):
    global translation, scaling_factor, rotation_angle, rotation_axis, shearing_factors, current_transformation
    if key == glfw.KEY_UP and action == glfw.PRESS:
        if current_transformation == 'translation':
            translation[1] += 0.1
    elif key == glfw.KEY_DOWN and action == glfw.PRESS:
        if current_transformation == 'translation':
            translation[1] -= 0.1
    elif key == glfw.KEY_LEFT and action == glfw.PRESS:
        if current_transformation == 'translation':
            translation[0] -= 0.1
        elif current_transformation == 'shearing':
            shearing_factors[0] -= 0.1
    elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
        if current_transformation == 'translation':
            translation[0] += 0.1
        elif current_transformation == 'shearing':
            shearing_factors[0] += 0.1
    elif key == glfw.KEY_W and action == glfw.PRESS:
        if current_transformation == 'translation':
            translation[2] += 0.1
    elif key == glfw.KEY_S and action == glfw.PRESS:
        if current_transformation == 'translation':
            translation[2] -= 0.1
    elif key == glfw.KEY_Z and action == glfw.PRESS:
        if current_transformation == 'scaling':
            scaling_factor += 0.1
        elif current_transformation == 'rotation':
            rotation_axis = [0, 0, 1]
            rotation_angle += 15
    elif key == glfw.KEY_X and action == glfw.PRESS:
        if current_transformation == 'scaling':
            scaling_factor -= 0.1
        elif current_transformation == 'rotation':
            rotation_axis = [1, 0, 0]
            rotation_angle += 15
    elif key == glfw.KEY_Y and action == glfw.PRESS:
        if current_transformation == 'rotation':
            rotation_axis = [0, 1, 0]
            rotation_angle += 15
    elif key == glfw.KEY_M and action == glfw.PRESS:
        main_menu(window)

def main_menu(window):
    global current_transformation
    print("\nMain Menu:")
    print("1. Translation")
    print("2. Scaling")
    print("3. Rotation")
    print("4. Shearing")
    print("5. Exit")
    choice = input("Select a transformation (1-5): ")

    if choice == '1':
        current_transformation = 'translation'
        print("Use arrow keys to translate the cube. Press 'W' and 'S' to move along the Z-axis.")
    elif choice == '2':
        current_transformation = 'scaling'
        print("Press 'Z' to increase and 'X' to decrease scaling.")
    elif choice == '3':
        current_transformation = 'rotation'
        print("Press 'X', 'Y', or 'Z' to rotate around the respective axis.")
    elif choice == '4':
        current_transformation = 'shearing'
        print("Use left and right arrow keys to shear along the Y-axis.")
    elif choice == '5':
        glfw.set_window_should_close(window, True)
    else:
        print("Invalid choice. Please try again.")
        main_menu(window)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "3D Transformations", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    main_menu(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        display()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
#use arrow Keys for the translation movements explicitly
#use Z for scale up & X for scale down
#use X, Y, & Z for the required rotation
#use Left & Right arrow keys for shearing