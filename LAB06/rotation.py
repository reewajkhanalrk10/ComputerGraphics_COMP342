import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Tetrahedron vertices
vertices = [
    [1, 1, 1],
    [-1, -1, 1],
    [1, -1, -1],
    [-1, 1, -1]
]

# Tetrahedron edges
edges = [
    [0, 1],
    [0, 2],
    [0, 3],
    [1, 2],
    [1, 3],
    [2, 3]
]

# Tetrahedron faces
faces = [
    [0, 1, 2],  # Front face
    [0, 1, 3],  # Left face
    [0, 2, 3],  # Right face
    [1, 2, 3]   # Bottom face
]

# Translation vector
translation = [0.0, 0.0, 0.0]

# Scaling factor for the tetrahedron
scaling_factor = 0.3  # Adjust the scaling factor here

# Rotation axis
rotation_axis = [1, 0, 0]  # Rotate around X-axis initially

# Rotation angle
rotation_angle = 0  # No initial rotation

# Point to rotate around
rotate_point = vertices[0]  # Right vertex of the tetrahedron

def draw_tetrahedron():
    # Draw faces with color
    glBegin(GL_TRIANGLES)
    for face in faces:
        glColor3fv([(v + 1) / 4 for v in face])  # Adjust color based on face index
        for vertex in face:
            glVertex3fv([(v * scaling_factor) + t for v, t in zip(vertices[vertex], translation)])  # Scale and translate each vertex
    glEnd()
    
    # Draw edges
    glColor3f(1.0, 1.0, 1.0)  # Edge color
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv([(v * scaling_factor) + t for v, t in zip(vertices[vertex], translation)])  # Scale and translate each vertex
    glEnd()

def apply_translation():
    draw_tetrahedron()

def apply_rotation():
    global rotation_axis, rotation_angle
    glPushMatrix()
    
    # Translate to the rotation point
    glTranslatef(rotate_point[0], rotate_point[1], rotate_point[2])
    
    # Perform rotation
    glRotatef(rotation_angle, *rotation_axis)  # Rotate around the specified axis by the given angle
    
    # Translate back to the original position
    glTranslatef(-rotate_point[0], -rotate_point[1], -rotate_point[2])
    
    draw_tetrahedron()
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)  # Camera position

    apply_translation()
    apply_rotation()

    glFlush()

def key_callback(window, key, scancode, action, mods):
    global rotation_angle, rotation_axis
    if action == glfw.PRESS:
        if key == glfw.KEY_X:
            rotation_axis = [1, 0, 0]  # Rotate around X-axis
        elif key == glfw.KEY_Y:
            rotation_axis = [0, 1, 0]  # Rotate around Y-axis
        elif key == glfw.KEY_Z:
            rotation_axis = [0, 0, 1]  # Rotate around Z-axis
        elif key == glfw.KEY_RIGHT:
            rotation_angle += 45  # Increment rotation angle by 90 degrees
            
def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "3D Transformations", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glClearColor(0.0, 0.0, 0.0, 0.0)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        display()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
