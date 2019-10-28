# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

from SETTINGS import *

from GameObjects.GameCube import GameCube
from GameObjects.SandCube import SandCube

class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
        # Hide cursor and lock mouse
        # Commenta þetta út ef það er pirrandi í development.
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(0, 3, 10), Point(0, 0, 0), Vector(0, 1, 0))

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(pi/2, 800/600, 0.02, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()

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
            "JUMP": False
        }

        self.texture_id01_brick = self.load_texture(sys.path[0] + "/textures/bricks.jpg")
        self.texture_id02_graybrick = self.load_texture(sys.path[0] + "/textures/graybricks.jpg")
        self.bind_textures()

        # Velocity
        self.v = VELOCITY
        # Mass
        self.m = MASS

        #Initialize variable that tracks how much mouse movement there is each frame
        self.mouse_move = (0, 0)
        #bool to ignore first mouse movement
        self.first_move = True



        self.white_background = False

        self.hand_angle_x = -1
        self.hand_angle_z = 0

    def load_texture(self, path):
        surface = pygame.image.load(path)
        tex_string = pygame.image.tostring(surface, "RGBA", 1)
        tex_width = surface.get_width()
        tex_height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_width, tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        return tex_id

    def bind_textures(self):
        """
        Binds all textures to a number, texture can then be accessed
        via self.shader.set_diffuse_texture(n)
        """

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id01_brick)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id02_graybrick)

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time

        self.jump(delta_time)

        if self.inputs["W"]:
            self.view_matrix.slide(0, 0, -2 * delta_time)
        if self.inputs["S"]:
            self.view_matrix.slide(0, 0, 2 * delta_time)
        if self.inputs["A"]:
            self.view_matrix.slide(-2 * delta_time, 0, 0)
        if self.inputs["D"]:
            self.view_matrix.slide(2 * delta_time, 0, 0)
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

        self.mouse_look_movement(delta_time)
        self.mouse_angle_x  = 0
        self.mouse_angle_y  = 0

    def mouse_look_movement(self, delta_time):
        """
        Function that handles looking around the game using mouse movement
        param delta_time: Elapsed time since last frame
        """

        #TODO SENSITIVITY constant er 0.1, revisit til að finna rétta sensið
        #TODO rotateY og pitch virka ekki eins, hugsanlega hafa sitthvoran constant
        # ef að það er mikill munur á mouse movement upp/niður vs vinstri/hægri

        # Change where the camera is looking based on how much mouse movement
        # there has been since last frame
        if self.mouse_move != (0, 0):
            self.hand_angle_z  -= (self.mouse_move[0] * SENSITIVITY) * delta_time
            self.hand_angle_x  -= (self.mouse_move[1] * SENSITIVITY) * delta_time
            if self.mouse_move[0] < 0:
                self.view_matrix.rotateY((self.mouse_move[0] * SENSITIVITY) * delta_time)
            elif self.mouse_move[0] > 0:
                self.view_matrix.rotateY((self.mouse_move[0] * SENSITIVITY) * delta_time)
            if self.mouse_move[1] < 0:
                # Make sure the player can not look further than straight up
                if self.view_matrix.n.y > -0.99:
                    self.view_matrix.pitch((self.mouse_move[1] * SENSITIVITY) * delta_time)
            elif self.mouse_move[1] > 0:
                # Make sure the player can not look further than straight down
                if self.view_matrix.n.y < 0.99:
                    self.view_matrix.pitch((self.mouse_move[1] * SENSITIVITY) * delta_time)
        # Reset to avoid camera pan
        self.mouse_move = (0, 0)

    def jump(self, delta_time):
        """
        Function that handles jumping physics
        param delta_time: Elapsed time since last frame

        Function uses a simple velocity * mass formula to calculate a jumping curve
        """

        if self.inputs["JUMP"]:
            # Momentum = mass * velocity
            p = (self.m * self.v)

            # Change position
            self.view_matrix.eye.y += p * delta_time
            # Change velocity
            self.v = self.v - 1

            # Hugsanlega skoða það að breyta hvernig annað movement virkar
            # A meðan player er að hoppa?
            #TODO hafa annað condition fyrir til að stoppa jump ef player
            #collide-ar við eitthvað fyrir neðan sig???

            # Stop the jump when it reaches the bottom of the 'curve'
            if self.v == -VELOCITY - 1:
                self.inputs["JUMP"] = False
                self.v = VELOCITY
  
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
        self.shader.set_light_position(*self.view_matrix.eye)
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)

        self.shader.set_light_specular(0.5, 0.5, 0.5)
        self.shader.set_material_specular(0.4, 0.4, 0.4)
        self.shader.set_light_ambient(0.4, 0.4, 0.4)
        self.shader.set_material_shininess(4)

        self.model_matrix.load_identity()

        self.cube.set_vertices(self.shader)

        self.shader.set_material_diffuse(1.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(9.0, 5.0, -2.0)
        self.model_matrix.add_scale(2.0, 2.0, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        # Small cube
        self.shader.set_using_texture(1.0)

        self.shader.set_diffuse_texture(0) 

        self.model_matrix.push_matrix()
        self.shader.set_material_diffuse(0.5, 0.5, 0.5)
        self.model_matrix.add_translation(0, 0, 0)
        self.model_matrix.add_scale(0.2, 0.2, 0.2)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        self.shader.set_diffuse_texture(1)

        self.shader.set_using_texture(0.0)
        # Player hand
        '''
        self.model_matrix.push_matrix()
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.model_matrix.add_translation(self.view_matrix.eye.x + 0.0397, self.view_matrix.eye.y - 0.0622, self.view_matrix.eye.z - 0.0384)
        self.model_matrix.add_x_rotation(self.hand_angle_x)
        self.model_matrix.add_y_rotation(-0.4)
        self.model_matrix.add_z_rotation(self.hand_angle_z)
        self.model_matrix.add_scale(0.02, 0.1, 0.05)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        '''

        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
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
                        self.inputs["JUMP"] = True
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

            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()
