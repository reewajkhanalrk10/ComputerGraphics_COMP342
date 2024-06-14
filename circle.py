import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

def draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # Clear the screen
    gl.glColor3f(1.0, 0.0, 0.0)        # Set drawing color to red
    gl.glBegin(gl.GL_TRIANGLES)        # Begin drawing triangles
    gl.glVertex2f(-0.5, -0.5)          # Specify triangle vertices
    gl.glVertex2f(0.5, -0.5)
    gl.glVertex2f(0.0, 0.5)
    gl.glEnd()                         # End drawing

def main():
    glut.glutInit()                     # Initialize GLUT
    display_mode = glut.GLUT_DOUBLE | glut.GLUT_RGB  # Set display mode (double buffering, RGB colors)
    glut.glutInitDisplayMode(display_mode)
    glut.glutInitWindowSize(640, 480)   # Set window size
    glut.glutInitWindowPosition(100, 100)  # Set window position
    glut.glutCreateWindow("My OpenGL Window")  # Create the window
    glut.glutDisplayFunc(draw)           # Set the display callback function
    glut.glutMainLoop()                  # Enter the main loop

if __name__ == "__main__":
    main()
