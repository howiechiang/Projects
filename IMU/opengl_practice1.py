#!/usr/bin/python

import pygame
import urllib
from OpenGL.GL import *
from OpenGL.GLU import *
from math import radians
from pygame.locals import *

class Cube(object):

    def __init__(self, position, color):
        self.position = position
        self.color = color

    num_faces = 6

    # Define Vertices
    vertices = [
        (-1,-0.05,-0.5),  # 0
        (-1,-0.05, 0.5),  # 1
        (-1, 0.05,-0.5),  # 2
        (-1, 0.05, 0.5),  # 3
        ( 1,-0.05,-0.5),  # 4
        ( 1,-0.05, 0.5),  # 5
        ( 1, 0.05,-0.5),  # 6
        ( 1, 0.05, 0.5)   # 7
        ]

    # Define Surfaces
    surfaces = [
        (0, 1, 3, 2),  # Left Wall
        (4, 5, 7, 6),  # Right Wall
        (0, 1, 5, 4),  # Bottom Wall
        (2, 3, 7, 6),  # Top Wall
        (0, 2, 6, 4),  # Back Wall
        (1, 3, 7, 5)   # Front Wall
    ]

    normals = [
        (-1.0, 0.0, 0.0),
        ( 1.0, 0.0, 0.0),
        ( 0.0,-1.0, 0.0),
        ( 0.0, 1.0, 0.0),
        ( 0.0, 0.0,-1.0),
        ( 0.0, 0.0, 1.0)
    ]

    # Define Edges based on the vertices in vertices()
    edges = [
        (0, 1),
        (0, 2),
        (0, 4),
        (1, 3),
        (1, 5),
        (2, 3),
        (2, 6),
        (3, 7),
        (4, 5),
        (4, 6),
        (5, 7),
        (6, 7)
    ]

    def render(self):
        # Build Surfaces
        glBegin(GL_QUADS) # delimit the array of vertices to define surface
        i = 0

        for surface in self.surfaces:
           glNormal3dv(self.normals[i])
           i+=1
           for vertex in surface:
               glVertex3fv(self.vertices[vertex])
        glEnd()

        # Build Edges
        glColor3fv((1, 1, 1))
        glLineWidth(2)
        glBegin(GL_LINES) # delimit the array of vertices to define lines
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

########################################################################################################################
# Functions for OpenGL
########################################################################################################################

def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / height, 0.001, 10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 1.0, -5.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0));

def gridLines():
    glColor3fv((1, 1, 1))
    glLineWidth(2)

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

    # for z in range(-10, 12, 2):
    #     glVertex3f(2, -1, z / 10.)
    #     glVertex3f(2, 1, z / 10.)

    for y in range(-10, 12, 2):
        glVertex3f(-2, y / 10., 1)
        glVertex3f(2, y / 10., 1)

    for y in range(-10, 12, 2):
        glVertex3f(-2, y / 10., 1)
        glVertex3f(-2, y / 10., -1)

    # for y in range(-10, 12, 2):
    #     glVertex3f(2, y / 10., 1)
    #     glVertex3f(2, y / 10., -1)

    glEnd()


########################################################################################################################
# Functions for OpenGL
########################################################################################################################

def read_values():
    link = "http://192.168.2.22:8080" # Change this address to your settings
    f = urllib.urlopen(link)
    myfile = f.read()
    return myfile.split(" ")



def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, HWSURFACE | DOUBLEBUF | OPENGL) # initialize screen size and notify pygame type of code it will be recieving
    resize(*display)
    init()
    # gluPerspective(45, (display[0] / display[1]), 0.001, 50.0)
    # glTranslatef(0.0, 0.0, -5)

    cube = Cube((0.0, 0.0, 0.0), (0.5, 0.5, 0.7))

    i =0

    while True:

        ################################################################################################################
        # Pygame Controls
        ################################################################################################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Checks if any buttons are pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotate(5, 0, 1, 0)
                if event.key == pygame.K_RIGHT:
                    glRotate(5, 0, -1, 0)
                # if event.key == pygame.K_UP:
                #     glRotate(5, -1, 0, 0)
                # if event.key == pygame.K_DOWN:
                #     glRotate(5,  1, 0, 0)

        # #Obtain camera position
        # pos = glGetDoublev(GL_MODELVIEW_MATRIX)
        # camera_x = pos[3][0]
        # camera_y = pos[3][1]
        # camera_z = pos[3][2]


        ################################################################################################################
        # OpenGL Image Update
        ################################################################################################################

        values = read_values()
        x_angle = values[0]
        y_angle = values[1]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear previous image
        gridLines()
        glPushMatrix()

        glRotate(float(x_angle), 1, 0, 0)
        glRotate(-float(y_angle), 0, 0, 1)

        cube.render()
        glPopMatrix()
        pygame.display.flip() # update display surface
        #pygame.time.wait(10)

main()
