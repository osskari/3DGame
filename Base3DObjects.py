import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *

import numpy


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.z * other)

    def __iter__(self):
        return (self.__getitem__(x) for x in range(3))

    def __getitem__(self, item):
        if item == 0 or item == "X":
            return self.x
        elif item == 1 or item == "Y":
            return self.y
        elif item == 2 or item == "Z":
            return self.z

    def __str__(self):
        return "Point(x: " + str(self.x) + ", y: " + str(self.y) + ", z: " + str(self.z) + ")"

    def __repr__(self):
        return "Point(x: " + str(self.x) + ", y: " + str(self.y) + ", z: " + str(self.z) + ")"

    def __eq__(self, other):
        return Point(self.x, self.y, self.z)


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        length = self.__len__()
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return self

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def __str__(self):
        return "Vector(x: " + str(self.x) + ", y: " + str(self.y) + ", z: " + str(self.z) + ")"

    def __repr__(self):
        return "Vector(x: " + str(self.x) + ", y: " + str(self.y) + ", z: " + str(self.z) + ")"


class Cube:
    def __init__(self):
        self.position_array = [-0.5, -0.5, -0.5,
                               -0.5, 0.5, -0.5,
                               0.5, 0.5, -0.5,
                               0.5, -0.5, -0.5,
                               -0.5, -0.5, 0.5,
                               -0.5, 0.5, 0.5,
                               0.5, 0.5, 0.5,
                               0.5, -0.5, 0.5,
                               -0.5, -0.5, -0.5,
                               0.5, -0.5, -0.5,
                               0.5, -0.5, 0.5,
                               -0.5, -0.5, 0.5,
                               -0.5, 0.5, -0.5,
                               0.5, 0.5, -0.5,
                               0.5, 0.5, 0.5,
                               -0.5, 0.5, 0.5,
                               -0.5, -0.5, -0.5,
                               -0.5, -0.5, 0.5,
                               -0.5, 0.5, 0.5,
                               -0.5, 0.5, -0.5,
                               0.5, -0.5, -0.5,
                               0.5, -0.5, 0.5,
                               0.5, 0.5, 0.5,
                               0.5, 0.5, -0.5]
        self.normal_array = [0.0, 0.0, -1.0,
                             0.0, 0.0, -1.0,
                             0.0, 0.0, -1.0,
                             0.0, 0.0, -1.0,
                             0.0, 0.0, 1.0,
                             0.0, 0.0, 1.0,
                             0.0, 0.0, 1.0,
                             0.0, 0.0, 1.0,
                             0.0, -1.0, 0.0,
                             0.0, -1.0, 0.0,
                             0.0, -1.0, 0.0,
                             0.0, -1.0, 0.0,
                             0.0, 1.0, 0.0,
                             0.0, 1.0, 0.0,
                             0.0, 1.0, 0.0,
                             0.0, 1.0, 0.0,
                             -1.0, 0.0, 0.0,
                             -1.0, 0.0, 0.0,
                             -1.0, 0.0, 0.0,
                             -1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0]
        self.uv_array = [0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0]

    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def draw(self):
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)


class OptimizedCube:
    def __init__(self):
        vertex_array = [
            -0.5, -0.5, -0.5,
            0.0, 0.0, -1.0,
            0.0, 0.0,
            -0.5, 0.5, -0.5,
            0.0, 0.0, -1.0,
            0.0, 1.0,
            0.5, 0.5, -0.5,
            0.0, 0.0, -1.0,
            1.0, 1.0,
            0.5, -0.5, -0.5,
            0.0, 0.0, -1.0,
            1.0, 0.0,
            -0.5, -0.5, 0.5,
            0.0, 0.0, 1.0,
            0.0, 0.0,
            -0.5, 0.5, 0.5,
            0.0, 0.0, 1.0,
            0.0, 1.0,
            0.5, 0.5, 0.5,
            0.0, 0.0, 1.0,
            1.0, 1.0,
            0.5, -0.5, 0.5,
            0.0, 0.0, 1.0,
            1.0, 0.0,
            -0.5, -0.5, -0.5,
            0.0, -1.0, 0.0,
            0.0, 0.0,
            0.5, -0.5, -0.5,
            0.0, -1.0, 0.0,
            0.0, 1.0,
            0.5, -0.5, 0.5,
            0.0, -1.0, 0.0,
            1.0, 1.0,
            -0.5, -0.5, 0.5,
            0.0, -1.0, 0.0,
            1.0, 0.0,
            -0.5, 0.5, -0.5,
            0.0, 1.0, 0.0,
            0.0, 0.0,
            0.5, 0.5, -0.5,
            0.0, 1.0, 0.0,
            0.0, 1.0,
            0.5, 0.5, 0.5,
            0.0, 1.0, 0.0,
            1.0, 1.0,
            -0.5, 0.5, 0.5,
            0.0, 1.0, 0.0,
            1.0, 0.0,
            -0.5, -0.5, -0.5,
            -1.0, 0.0, 0.0,
            0.0, 0.0,
            -0.5, -0.5, 0.5,
            -1.0, 0.0, 0.0,
            0.0, 1.0,
            -0.5, 0.5, 0.5,
            -1.0, 0.0, 0.0,
            1.0, 1.0,
            -0.5, 0.5, -0.5,
            -1.0, 0.0, 0.0,
            1.0, 0.0,
            0.5, -0.5, -0.5,
            1.0, 0.0, 0.0,
            0.0, 0.0,
            0.5, -0.5, 0.5,
            1.0, 0.0, 0.0,
            0.0, 1.0,
            0.5, 0.5, 0.5,
            1.0, 0.0, 0.0,
            1.0, 1.0,
            0.5, 0.5, -0.5,
            1.0, 0.0, 0.0,
            1.0, 0.0
        ]
        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype="float32"), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def set_vertices(self, shader):
        shader.set_attribute_buffers_with_uv(self.vertex_buffer_id)

    def draw(self, shader):
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


class Sphere:
    def __init__(self, stacks=12, slices=24):
        self.vertex_array = []
        self.slices = slices

        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                self.vertex_array.append(sin(stack_angle) * cos(slice_angle))
                self.vertex_array.append(cos(stack_angle))
                self.vertex_array.append(sin(stack_angle) * sin(slice_angle))

                self.vertex_count += 2

    def set_vertices(self, shader):
        shader.set_position_attribute(self.vertex_array)
        shader.set_normal_attribute(self.vertex_array)

    def draw(self, shader):
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)


class OptimizedSphere:
    def __init__(self, stacks=12, slices=24):
        vertex_array = []
        self.slice = slices

        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                for _ in range(2):
                    vertex_array.append(sin(stack_angle) * cos(slice_angle))
                    vertex_array.append(cos(stack_angle))
                    vertex_array.append(sin(stack_angle) * sin(slice_angle))

                vertex_array.append(slice_count / slices)
                vertex_array.append(stack_count / stacks)

                for _ in range(2):
                    vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
                    vertex_array.append(cos(stack_angle + stack_interval))
                    vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))

                vertex_array.append(slice_count / slices)
                vertex_array.append((stack_count + 1) / stacks)

                self.vertex_count += 2

        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype="float32"), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        vertex_array = None


    def draw(self, shader):
        shader.set_attribute_buffers_with_uv(self.vertex_buffer_id)
        for i in range(0, self.vertex_count, (self.slice + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slice + 1) * 2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
