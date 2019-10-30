from math import *  # trigonometry

from aabbtree import AABB

from Base3DObjects import *


class ModelMatrix:
    def __init__(self):
        self.matrix = [1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1]
        self.stack = []
        self.stack_count = 0
        self.stack_capacity = 0

    def load_identity(self):
        self.matrix = [1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1]

    def copy_matrix(self):
        new_matrix = [0] * 16
        for i in range(16):
            new_matrix[i] = self.matrix[i]
        return new_matrix

    def add_transformation(self, matrix2):
        counter = 0
        new_matrix = [0] * 16
        for row in range(4):
            for col in range(4):
                for i in range(4):
                    new_matrix[counter] += self.matrix[row *
                                                       4 + i] * matrix2[col + 4 * i]
                counter += 1
        self.matrix = new_matrix

    def add_nothing(self):
        other_matrix = [1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_translation(self, x, y, z):
        other_matrix = [1, 0, 0, x,
                        0, 1, 0, y,
                        0, 0, 1, z,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_scale(self, sx, sy, sz):
        other_matrix = [sx, 0, 0, 0,
                        0, sy, 0, 0,
                        0, 0, sz, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_x_rotation(self, angle):
        c = cos(angle)
        s = sin(angle)
        other_matrix = [1, 0, 0, 0,
                        0, c, -s, 0,
                        0, s, c, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_y_rotation(self, angle):
        c = cos(angle)
        s = sin(angle)
        other_matrix = [c, 0, s, 0,
                        0, 1, 0, 0,
                        -s, 0, c, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_z_rotation(self, angle):
        c = cos(angle)
        s = sin(angle)
        other_matrix = [c, -s, 0, 0,
                        s, c, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def push_matrix(self):
        self.stack.append(self.copy_matrix())

    def pop_matrix(self):
        self.matrix = self.stack.pop()

    # This operation mainly for debugging
    def __str__(self):
        ret_str = ""
        counter = 0
        for _ in range(4):
            ret_str += "["
            for _ in range(4):
                ret_str += " " + str(self.matrix[counter]) + " "
                counter += 1
            ret_str += "]\n"
        return ret_str


# The ViewMatrix class holds the camera's coordinate frame and
# set's up a transformation concerning the camera's position
# and orientation

class ViewMatrix:
    def __init__(self):
        self.eye = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)
        self.bound = (0.3, 3, 0.3)

    def look(self, eye, center, up):
        self.eye = eye
        self.n = (eye - center)
        self.n.normalize()
        self.u = up.cross(self.n)
        self.u.normalize()
        self.v = self.n.cross(self.u)

    def walk(self, del_u, del_v, del_n):
        vec = Vector(0, 1, 0).cross(self.u)
        self.eye.x -= del_n * vec.x
        self.eye.z -= del_n * vec.z
        return self.eye

    def slide(self, del_u, del_v, del_n):
        return self.eye + self.u * del_u + self.v * del_v + self.n * del_n

    def roll(self, angle):
        c = cos(angle)
        s = sin(angle)

        tmp_u = self.u * c + self.v * s
        self.v = self.u * -s + self.v * c
        self.u = tmp_u

    def pitch(self, angle):
        c = cos(angle)
        s = sin(angle)

        tmp_v = self.v * c + self.n * -s
        self.n = self.v * s + self.n * c
        self.v = tmp_v

    def yaw(self, angle):
        c = cos(angle)
        s = sin(angle)

        tmp_u = self.u * c + self.n * s
        self.n = self.u * -s + self.n * c
        self.u = tmp_u

    def rotateY(self, angle):
        """
        rotates the camera yaw style regardless of the camera looking up/down
        """
        #radians = angle * (pi / 180)
        c = cos(angle)
        s = sin(angle)
        self.u = Vector(c * self.u.x - s * self.u.z,
                        self.u.y, s * self.u.x + c * self.u.z)
        self.v = Vector(c * self.v.x - s * self.v.z,
                        self.v.y, s * self.v.x + c * self.v.z)
        self.n = Vector(c * self.n.x - s * self.n.z,
                        self.n.y, s * self.n.x + c * self.n.z)

    def get_matrix(self):
        minusEye = Vector(-self.eye.x, -self.eye.y, -self.eye.z)
        return [self.u.x, self.u.y, self.u.z, minusEye.dot(self.u),
                self.v.x, self.v.y, self.v.z, minusEye.dot(self.v),
                self.n.x, self.n.y, self.n.z, minusEye.dot(self.n),
                0, 0, 0, 1]


# The ProjectionMatrix class builds transformations concerning
# the camera's "lens"

class ProjectionMatrix:
    def __init__(self):
        self.left = -1
        self.right = 1
        self.bottom = -1
        self.top = 1
        self.near = -1
        self.far = 1

        self.is_orthographic = True

    def set_perspective(self, fovy, aspect, near, far):
        self.near = near
        self.far = far
        self.top = near * tan(fovy / 2)
        self.bottom = -self.top
        self.right = self.top * aspect
        self.left = -self.right
        self.is_orthographic = False

    def set_orthographic(self, left, right, bottom, top, near, far):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far
        self.is_orthographic = True

    def get_matrix(self):
        if self.is_orthographic:
            A = 2 / (self.right - self.left)
            B = -(self.right + self.left) / (self.right - self.left)
            C = 2 / (self.top - self.bottom)
            D = -(self.top + self.bottom) / (self.top - self.bottom)
            E = 2 / (self.near - self.far)
            F = (self.near + self.far) / (self.near - self.far)

            return [A, 0, 0, B,
                    0, C, 0, D,
                    0, 0, E, F,
                    0, 0, 0, 1]

        else:
            A = (2 * self.near) / (self.right - self.left)
            B = (self.right + self.left) / (self.right - self.left)
            C = (2 * self.near) / (self.top - self.bottom)
            D = (self.top + self.bottom) / (self.top - self.bottom)
            E = -(self.far + self.near) / (self.far - self.near)
            F = -(2 * self.far * self.near) / (self.far - self.near)
            return [A, 0, B, 0,
                    0, C, D, 0,
                    0, 0, E, F,
                    0, 0, -1, 0]
