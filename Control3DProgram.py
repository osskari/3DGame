# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from aabbtree import AABB, AABBTree

from Shaders import *
from Matrices import *


class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(0, 3, 10), Point(0, 0, 0), Vector(0, 1, 0))

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(pi/2, 800/600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.tree = AABBTree()

        self.cube1 = (Point(9.0, 5.0, -2.0), (2.0, 2.0, 2.0),
                      (1.0, 0.5, 0.0), (1.0, 1.0, 1.0), 13)
        self.tree.add(
            AABB([(9.0-2.0, 9.0+2.0), (5.0-2.0, 5.0+2.0), (-2.0-2.0, -2.0+2.0)]))
        self.cube2 = (Point(-5.0, -0.8, -5.0), (10.0, 0.8, 10.0),
                      (0.0, 1.0, 0.0), (1.0, 1.0, 1.0), 13)
        self.tree.add(
            AABB([(-5.0-10.0, -5.0+10.0), (-0.8-0.8, -0.8+0.8), (-5.0-10.0, -5.0+10.0)]))

        self.inputs = {
            "W": False,
            "A": False,
            "S": False,
            "D": False,
            "UP": False,
            "DOWN": False,
            "LEFT": False,
            "RIGHT": False,
            "Q": False,
            "E": False
        }

        self.white_background = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        # if angle > 2 * pi:
        #     angle -= (2 * pi)

        if self.inputs["W"]:
            self.view_matrix.slide(0, 0, -10 * delta_time)
        if self.inputs["S"]:
            self.view_matrix.slide(0, 0, 10 * delta_time)
        if self.inputs["A"]:
            self.view_matrix.slide(-10 * delta_time, 0, 0)
        if self.inputs["D"]:
            self.view_matrix.slide(10 * delta_time, 0, 0)
        if self.inputs["Q"]:
            self.view_matrix.roll(pi * delta_time)
        if self.inputs["E"]:
            self.view_matrix.roll(-pi * delta_time)
        if self.inputs["UP"]:
            self.view_matrix.pitch(-pi * delta_time)
        if self.inputs["DOWN"]:
            self.view_matrix.pitch(pi * delta_time)
        if self.inputs["LEFT"]:
            self.view_matrix.yaw(-pi * delta_time)
        if self.inputs["RIGHT"]:
            self.view_matrix.yaw(pi * delta_time)
        eyebound = (self.view_matrix.eye.x, self.view_matrix.eye.y,
                    self.view_matrix.eye.z, 0.2)
        if(self.tree.does_overlap(AABB([(eyebound[0] - eyebound[3], eyebound[0] + eyebound[3]), (eyebound[1] - eyebound[3], eyebound[1] + eyebound[3]), (eyebound[2] - eyebound[3], eyebound[2] + eyebound[3])]))):
            print("hebbo")

    def display(self):
        glEnable(GL_DEPTH_TEST)

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # self.shader.set_light_position(*self.view_matrix.eye)
        self.shader.set_eye_position(*self.view_matrix.eye)
        self.shader.set_light_position(*Point(0, 10, 0))
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)

        self.shader.set_light_specular(1.0, 1.0, 1.0)
        self.shader.set_material_specular(1.0, 1.0, 1.0)
        self.shader.set_material_shininess(13)

        self.model_matrix.load_identity()

        self.cube.set_vertices(self.shader)

        self.shader.set_material_diffuse(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(9.0, 5.0, -2.0)
        self.model_matrix.add_scale(2.0, 2.0, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        self.shader.set_material_diffuse(0.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-5.0, -0.8, -5.0)
        self.model_matrix.add_scale(10.0, 0.8, 10.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        pygame.display.flip()

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                    if event.key == K_w:
                        self.inputs["W"] = True
                    if event.key == K_s:
                        self.inputs["S"] = True
                    if event.key == K_a:
                        self.inputs["A"] = True
                    if event.key == K_d:
                        self.inputs["D"] = True
                    if event.key == K_q:
                        self.inputs["Q"] = True
                    if event.key == K_e:
                        self.inputs["E"] = True
                    if event.key == K_UP:
                        self.inputs["UP"] = True
                    if event.key == K_DOWN:
                        self.inputs["DOWN"] = True
                    if event.key == K_LEFT:
                        self.inputs["LEFT"] = True
                    if event.key == K_RIGHT:
                        self.inputs["RIGHT"] = True
                elif event.type == pygame.KEYUP:
                    if event.key == K_w:
                        self.inputs["W"] = False
                    if event.key == K_s:
                        self.inputs["S"] = False
                    if event.key == K_a:
                        self.inputs["A"] = False
                    if event.key == K_d:
                        self.inputs["D"] = False
                    if event.key == K_q:
                        self.inputs["Q"] = False
                    if event.key == K_e:
                        self.inputs["E"] = False
                    if event.key == K_UP:
                        self.inputs["UP"] = False
                    if event.key == K_DOWN:
                        self.inputs["DOWN"] = False
                    if event.key == K_LEFT:
                        self.inputs["LEFT"] = False
                    if event.key == K_RIGHT:
                        self.inputs["RIGHT"] = False

            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()
