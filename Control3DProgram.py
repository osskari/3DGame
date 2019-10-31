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

from SETTINGS import *
from HelperObjects import BezierMotion
from Map import *

from GameObjects.Sky import *

from GameObjects.GameCube import GameCube
from GameObjects.SandCube import SandCube
from GameObjects.Projectile import Projectile


class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
        # Hide cursor and lock mouse
        # Commenta þetta út ef það er pirrandi í development.
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        self.sky_shader = SkyShader3D()
        self.sky_shader.use()

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(0, 6, 10), Point(0, 0, 0), Vector(0, 1, 0))

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(pi / 2, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = OptimizedCube()

        self.sphere = OptimizedSphere()

        self.sky_sphere = SkySphere(128, 256)

        # Timer for bezier curves
        self.timer = 0.0
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

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
            "E": False,
            "JUMP": False,
            "G": False,
            "CLICK": False
        }


        self.sunMotion = BezierMotion(
            -30,
            30,
            Point(-50.0, -30.0, 0.0),
            Point(-50.0, 30.0, 10.0),
            Point(50.0, 30.0, 10.0),
            Point(50.0, -30.0, 0.0),
            Point(0.0, -40.0, -10.0),
            Point(-50.0, -30.0, 0.0)
        )

        self.moonMotion = BezierMotion(
            0,
            60,
            Point(-50.0, -50.0, 0.0),
            Point(-50.0, 50.0, 10.0),
            Point(50.0, 50.0, 10.0),
            Point(50.0, -50.0, 0.0),
            Point(0.0, -40.0, -10.0),
            Point(-50.0, -30.0, 0.0)
        )


        self.texture_id00_brick = self.load_texture(
            sys.path[0] + "/textures/bricks.jpg")
        self.texture_id01_graybrick = self.load_texture(
            sys.path[0] + "/textures/graybricks.jpg")
        self.texture_sun = self.load_texture(
            sys.path[0] + "/textures/2k_sun.jpg")
        self.texture_moon = self.load_texture(
            sys.path[0] + "/textures/2k_moon.jpg")
        self.texture_sky = self.load_texture(
            sys.path[0] + "/textures/sky_sphere_tex3.jpg")
    
        self.bind_textures()
        self.sun = CircularObject(self.texture_sun, self.sunMotion.get_current_position(0), self.sunMotion)
        self.moon = CircularObject(self.texture_moon, self.moonMotion.get_current_position(0), self.moonMotion)

        self.map = Map({"texture": self.texture_sun, "currentpos": self.sunMotion.get_current_position(0), "motion": self.sunMotion}, 
                       {"texture": self.texture_moon, "currentpos": self.moonMotion.get_current_position(0), "motion": self.moonMotion})

        # Velocity
        self.v = VELOCITY
        self.gv = 0
        # Mass
        self.m = MASS

        # Initialize variable that tracks how much mouse movement there is each frame
        self.mouse_move = (0, 0)
        # bool to ignore first mouse movement
        self.first_move = True
        self.can_jump = True

        self.white_background = False

        self.projectiles = []

    def load_texture(self, path):
        surface = pygame.image.load(path)
        tex_string = pygame.image.tostring(surface, "RGBA", 1)
        tex_width = surface.get_width()
        tex_height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_width,
                     tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        return tex_id

    def bind_textures(self):
        """
        Binds all textures to a number, texture can then be accessed
        via self.shader.set_diffuse_texture(n)
        """

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id00_brick)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.texture_id01_graybrick)
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.texture_sun)
        glActiveTexture(GL_TEXTURE4)
        glBindTexture(GL_TEXTURE_2D, self.texture_moon)
        glActiveTexture(GL_TEXTURE5)
        glBindTexture(GL_TEXTURE_2D, self.texture_sky)

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        # Delay 'start' of gravity to advoid instaclipping on launch
        # self.jump() has it's own gravity, so disable this when a jump is occuring
        if self.timer != 0.0 and not self.inputs["JUMP"]:
            self.gravity(delta_time)

        self.timer += delta_time
        self.angle += pi * delta_time


        if self.inputs["W"]:
            newpos = self.view_matrix.walk(-10 * delta_time)
            player = self.map.tree.move({"pos": self.view_matrix.eye, 
                                                   "scale": self.view_matrix.bound, 
                                                   "direction": newpos - self.view_matrix.eye,
                                                   "newpos": newpos})
            self.view_matrix.eye += player["direction"]
            if self.inputs["JUMP"] and ((1,1,0) in player["collision"] or (0,1,1) in player["collision"]):
                self.can_jump = True
            if (0,0,0) in player["collision"]:
                self.view_matrix.eye = Point(1000, 5, 1000)
        if self.inputs["S"]:
            newpos = self.view_matrix.walk(10 * delta_time)
            player = self.map.tree.move({"pos": self.view_matrix.eye, 
                                                   "scale": self.view_matrix.bound, 
                                                   "direction": newpos - self.view_matrix.eye,
                                                   "newpos": newpos})
            self.view_matrix.eye += player["direction"]
            if self.inputs["JUMP"] and ((1,1,0) in player["collision"] or (0,1,1) in player["collision"]):
                self.can_jump = True
            if (0,0,0) in player["collision"]:
                self.view_matrix.eye = Point(1000, 5, 1000)
        if self.inputs["A"]:
            newpos = self.view_matrix.slide(-10 * delta_time, 0, 0)
            player = self.map.tree.move({"pos": self.view_matrix.eye, 
                                                   "scale": self.view_matrix.bound, 
                                                   "direction": newpos - self.view_matrix.eye,
                                                   "newpos": newpos})
            self.view_matrix.eye += player["direction"]
            if self.inputs["JUMP"] and ((1,1,0) in player["collision"] or (0,1,1) in player["collision"]):
                self.can_jump = True
            if (0,0,0) in player["collision"]:
                self.view_matrix.eye = Point(1000, 5, 1000)
        if self.inputs["D"]:
            newpos = self.view_matrix.slide(10 * delta_time, 0, 0)
            player = self.map.tree.move({"pos": self.view_matrix.eye, 
                                                   "scale": self.view_matrix.bound, 
                                                   "direction": newpos - self.view_matrix.eye,
                                                   "newpos": newpos})
            self.view_matrix.eye += player["direction"]
            if self.inputs["JUMP"] and ((1,1,0) in player["collision"] or (0,1,1) in player["collision"]):
                self.can_jump = True
            if (0,0,0) in player["collision"]:
                self.view_matrix.eye = Point(1000, 5, 1000)
        if self.inputs["JUMP"]:
            self.jump(delta_time)

        self.map.sun.bezier_done(self.timer)
        self.map.moon.bezier_done(self.timer)

        self.mouse_look_movement(delta_time)
        self.mouse_angle_x = 0
        self.mouse_angle_y = 0

    # Creates a downwards acceleration
    def gravity(self, delta_time):
        # Increase the downward momentum
        self.gv += -0.2 * delta_time
        # Move to the gravity with respect to collision
        newpos = Point(self.view_matrix.eye.x, self.view_matrix.eye.y + self.gv, self.view_matrix.eye.z)
        player = self.map.tree.move({"pos": self.view_matrix.eye, 
                                                "scale": self.view_matrix.bound, 
                                                "direction": newpos - self.view_matrix.eye,
                                                "newpos": newpos})
        self.view_matrix.eye += player["direction"]
        # Reset the downwards velocity when player lands on an object
        if (1,0,1) in player["collision"]:
            self.gv = 0
        if (0,0,0) in player["collision"]
            self.view_matrix.eye = Point(1000, 5, 1000)

    def mouse_look_movement(self, delta_time):
        """
        Function that handles looking around the game using mouse movement
        param delta_time: Elapsed time since last frame
        """

        # TODO SENSITIVITY constant er 0.1, revisit til að finna rétta sensið
        # TODO rotateY og pitch virka ekki eins, hugsanlega hafa sitthvoran constant
        # ef að það er mikill munur á mouse movement upp/niður vs vinstri/hægri

        # Change where the camera is looking based on how much mouse movement
        # there has been since last frame
        if self.mouse_move != (0, 0):
            if self.mouse_move[0] < 0:
                self.view_matrix.rotateY(
                    self.mouse_move[0] * SENSITIVITY * delta_time)
            elif self.mouse_move[0] > 0:
                self.view_matrix.rotateY(
                    self.mouse_move[0] * SENSITIVITY * delta_time)
            if self.mouse_move[1] < 0:
                # Make sure the player can not look further than straight up
                if self.view_matrix.n.y > -0.99:
                    self.view_matrix.pitch(
                        (self.mouse_move[1] * SENSITIVITY) * delta_time)
            elif self.mouse_move[1] > 0:
                # Make sure the player can not look further than straight down
                if self.view_matrix.n.y < 0.99:
                    self.view_matrix.pitch(
                        (self.mouse_move[1] * SENSITIVITY) * delta_time)
        # Reset to avoid camera pan
        self.mouse_move = (0, 0)

    def jump(self, delta_time):
        """
        Function that handles jumping physics
        param delta_time: Elapsed time since last frame

        Function uses a simple velocity * mass formula to calculate a jumping curve
        """
        # Momentum = mass * velocity
        p = (self.m * self.v)
        # Change position
        newpos = Point(self.view_matrix.eye.x, self.view_matrix.eye.y + (delta_time * p), self.view_matrix.eye.z)
        player = self.map.tree.move({"pos": self.view_matrix.eye, 
                                                "scale": self.view_matrix.bound, 
                                                "direction": newpos - self.view_matrix.eye,
                                                "newpos": newpos})
        self.view_matrix.eye += player["direction"]
        # Change velocity
        self.v = self.v - 13 * delta_time


        # Stop the jump when it reaches the bottom of the 'curve' or hits something
        if self.v == -VELOCITY - 1 or (1,0,1) in player["collision"]:
            self.inputs["JUMP"] = False
            self.v = VELOCITY
        if (0,0,0) in player["collision"]
            self.view_matrix.eye = Point(1000, 5, 1000)

    def display(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glViewport(0, 0, 800, 600)
        self.model_matrix.load_identity()

        glDisable(GL_DEPTH_TEST)

        self.sky_shader.use()
        self.sky_shader.set_diffuse_texture(5)
        self.sky_shader.set_alpha_texture(None)

        self.sky_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.sky_shader.set_view_matrix(self.view_matrix.get_matrix())
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)
        self.model_matrix.add_x_rotation(pi)
        #self.model_matrix.add_z_rotation(pi / 2)
        self.sky_shader.set_model_matrix(self.model_matrix.matrix)
        self.sky_sphere.draw(self.sky_shader)

        self.model_matrix.pop_matrix()
        self.model_matrix.load_identity()

        self.shader.use()
        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        # self.shader.set_light_position(*self.view_matrix.eye)
        self.shader.set_eye_position(*self.view_matrix.eye)
        self.shader.set_light_position(*self.view_matrix.eye)
        self.shader.set_light_diffuse(0.3, 0.3, 0.3)
        self.shader.set_light_specular(0.2, 0.2, 0.2)
        self.shader.set_global_ambient(0.2, 0.2, 0.2)

        self.shader.set_material_specular(0.4, 0.4, 0.4)
        self.shader.set_material_shininess(10)

        # Not using texture by default
        self.shader.set_using_texture(0.0)
        self.shader.set_using_specular_texture(0.0)

        ################ DRAW #################
        self.map.draw(self.shader, self.model_matrix, self.timer)

        pygame.display.flip()

    def program_loop(self):
        exiting = False
        while not exiting:
            pygame.mouse.set_pos = (400, 300)
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
                    if event.key == K_SPACE:
                        if self.can_jump:
                            self.v = VELOCITY
                            self.can_jump = False
                        self.inputs["JUMP"] = True
                    if event.key == K_g:
                        self.inputs["G"] = True
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
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_move = event.rel
                    if self.first_move:
                        self.mouse_move = (0, 0)
                        self.first_move = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.projectiles.append(
                        Projectile(self.view_matrix.eye, self.view_matrix.n, self.timer)
                    )

            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()
