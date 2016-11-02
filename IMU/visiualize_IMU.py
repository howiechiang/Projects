#!/usr/bin/python

import pygame
import urllib
from OpenGL.GL import *
from OpenGL.GLU import *
from math import radians
from pygame.locals import *

SCREEN_SIZE = (800, 600)

def set_view(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(1, 1.5, -5.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)

def grid():
    glLineWidth(0.5) # Line Thickness
    glBegin(GL_LINES)

    for x in range(-20, 22, 2):
        glVertex3f(x / 10., -1, -1)
        glVertex3f(x / 10., -1, 1)

    for x in range(-20, 22, 2):
        glVertex3f(x / 10., -1, 1)
        glVertex3f(x / 10., 1, 1)

    for z in range(-10, 12, 2):
        glVertex3f(-2, -1, z / 10.)
        glVertex3f(2, -1, z / 10.)

    for z in range(-10, 12, 2):
        glVertex3f(-2, -1, z / 10.)
        glVertex3f(-2, 1, z / 10.)

    for z in range(-10, 12, 2):
        glVertex3f(2, -1, z / 10.)
        glVertex3f(2, 1, z / 10.)

    for y in range(-10, 12, 2):
        glVertex3f(-2, y / 10., 1)
        glVertex3f(2, y / 10., 1)

    for y in range(-10, 12, 2):
        glVertex3f(-2, y / 10., 1)
        glVertex3f(-2, y / 10., -1)

    for y in range(-10, 12, 2):
        glVertex3f(2, y / 10., 1)
        glVertex3f(2, y / 10., -1)
    glEnd()


class Cube(object):

    def __init__(self, position, color):
        self.position = position
        self.color = color

    vertices = [ (-1.0, -0.05, 0.5),
                 (1.0, -0.05, 0.5),
                 (1.0, 0.05, 0.5),
                 (-1.0, 0.05, 0.5),
                 (-1.0, -0.05, -0.5),
                 (1.0, -0.05, -0.5),
                 (1.0, 0.05, -0.5),
                 (-1.0, 0.05, -0.5) ]

    normals = [ (0.0, 0.0, +1.0),  # front
                (0.0, 0.0, -1.0),  # back
                (+1.0, 0.0, 0.0),  # right
                (-1.0, 0.0, 0.0),  # left
                (0.0, +1.0, 0.0),  # top
                (0.0, -1.0, 0.0) ]  # bottom

    vertex_faces = [ (0, 1, 2, 3),  # front
                     (4, 5, 6, 7),  # back
                     (1, 5, 6, 2),  # right
                     (0, 4, 7, 3),  # left
                     (3, 2, 6, 7),  # top
                     (0, 1, 5, 4) ]  # bottom

    # Render the faces of the cube
    def render(self):

        glColor(self.color)

        glBegin(GL_QUADS) # Delimit the array of vertices to define face
        for face in self.vertex_faces:
            v1, v2, v3, v4 = face
            glVertex(self.vertices[v1])
            glVertex(self.vertices[v2])
            glVertex(self.vertices[v3])
            glVertex(self.vertices[v4])

        for normal in self.normals:
            glNormal3dv(normal)
        glEnd()



# Main Program
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    set_view(*SCREEN_SIZE)


    cube = Cube((0.0, 0.0, 0.0), (.5, .5, .5))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clears data buffers
        grid()
        
        cube.render()

        pygame.display.flip() # Update the display Surface
        pygame.time.wait(5)