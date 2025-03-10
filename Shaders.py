from OpenGL.GL import *
import OpenGL.GLU
from math import *  # trigonometry

import sys

import numpy

from Base3DObjects import *


class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader, shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if result != 1:  # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" +
                  str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader, shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if result != 1:  # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" +
                  str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.uvLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        # self.colorLoc = glGetUniformLocation(self.renderingProgramID, "u_color")
        self.eyePosLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        self.lightPosLoc = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecularLoc = glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        self.globalAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_global_ambient")

        self.sunPosLoc = glGetUniformLocation(self.renderingProgramID, "u_sun_position")
        self.sunDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_sun_diffuse")
        self.sunSpecularLoc = glGetUniformLocation(self.renderingProgramID, "u_sun_specular")
        self.sunAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_sun_ambient")

        self.moonPosLoc = glGetUniformLocation(self.renderingProgramID, "u_moon_position")
        self.moonDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_moon_diffuse")
        self.moonSpecularLoc = glGetUniformLocation(self.renderingProgramID, "u_moon_specular")
        self.moonAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_moon_ambient")

        self.materialDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.materialSpecularLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")

        self.modelMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")
        self.materialShininessLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_shininess")

        self.diffuseTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_tex01")
        self.specularTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_tex02")

        self.usingTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_using_texture")
        self.usingSpecularTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_using_specular_texture")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3,
                              GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, normal_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT,
                              True, 0, normal_array)

    def set_light_position(self, x, y, z):
        glUniform4f(self.lightPosLoc, x, y, z, 1.0)

    def set_light_diffuse(self, r, g, b):
        glUniform4f(self.lightDiffuseLoc, r, g, b, 1.0)

    def set_global_ambient(self, r, g, b):
        glUniform4f(self.globalAmbientLoc, r, g, b, 1.0)

    def set_light_specular(self, r, g, b):
        glUniform4f(self.lightSpecularLoc, r, g, b, 1.0)

    # Setting parameters for the light from the sun
    def set_sun_position(self, x, y, z):
        glUniform4f(self.sunPosLoc, x, y, z, 1.0)

    def set_sun_diffuse(self, r, g, b):
        glUniform4f(self.sunDiffuseLoc, r, g, b, 1.0)

    def set_sun_ambient(self, r, g, b):
        glUniform4f(self.sunAmbientLoc, r, g, b, 1.0)

    def set_sun_specular(self, r, g, b):
        glUniform4f(self.sunSpecularLoc, r, g, b, 1.0)

    # Setting parameters for the light from the moon
    def set_moon_position(self, x, y, z):
        glUniform4f(self.moonPosLoc, x, y, z, 1.0)

    def set_moon_diffuse(self, r, g, b):
        glUniform4f(self.moonDiffuseLoc, r, g, b, 1.0)

    def set_moon_ambient(self, r, g, b):
        glUniform4f(self.moonAmbientLoc, r, g, b, 1.0)

    def set_moon_specular(self, r, g, b):
        glUniform4f(self.moonSpecularLoc, r, g, b, 1.0)

    def set_material_diffuse(self, r, g, b):
        glUniform4f(self.materialDiffuseLoc, r, g, b, 1.0)

    def set_eye_position(self, x, y, z):
        glUniform4f(self.eyePosLoc, x, y, z, 1.0)

    def set_material_specular(self, r, g, b):
        glUniform4f(self.materialSpecularLoc, r, g, b, 1.0)

    def set_material_shininess(self, shininess):
        glUniform1f(self.materialShininessLoc, shininess)

    def set_attribute_buffers_with_uv(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat),
                              OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat),
                              OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))

    def set_uv_attribute(self, vertex_array):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)

    def set_using_texture(self, n):
        glUniform1f(self.usingTextureLoc, n)

    def set_using_specular_texture(self, n):
        glUniform1f(self.usingSpecularTextureLoc, n)

    def set_diffuse_texture(self, n):
        glUniform1i(self.diffuseTextureLoc, n)
    
    def set_specular_texture(self, n):
        glUniform1i(self.specularTextureLoc, n)


class SkyShader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/SkyShader.vert")
        glShaderSource(vert_shader, shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if result != 1:  # Sky shader didn't compile
            print("Couldn't compile vertex Sky shader\nShader compilation Log:\n" +
                  str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/SkyShader.frag")
        glShaderSource(frag_shader, shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if result != 1:  # Sky shader didn't compile
            print("Couldn't compile fragment Sky shader\nShader compilation Log:\n" +
                  str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)


        self.uvLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        self.modelMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        self.diffuseTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_tex01")
        self.alphaTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_tex02")

        self.usingAlphaTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_using_alpha_texture")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3,
                              GL_FLOAT, False, 0, vertex_array)

    def set_attribute_buffers_with_uv(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 5 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 5 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
    
    def set_diffuse_texture(self, n):
        glUniform1i(self.diffuseTextureLoc, n)

    def set_alpha_texture(self, n):
        if n == None:
            glUniform1f(self.usingAlphaTextureLoc, 0.0)
        else:
            glUniform1f(self.usingAlphaTextureLoc, 1.0)
            glUniform1i(self.alphaTextureLoc, n)
