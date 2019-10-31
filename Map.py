from HelperObjects import Collision
from Base3DObjects import Point, OptimizedCube as Cube, OptimizedSphere as Sphere
from GameObjects.Sky import CircularObject


class Map:
    def __init__(self, sun, moon):
        self.objects = [
            {
                "pos": Point(0, 0, 0),
                "scale": (20, 0.5, 20),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(10, 10, 0),
                "scale": (10, 2, 10),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(-20, 20, 0),
                "scale": (10, 2, 10),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(0, 40, 0),
                "scale": (10, 0.5, 10),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(0, 59.5, 0),
                "scale": (10, 0.5, 10),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(16, 70, 0),
                "scale": (0.5, 35, 30),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(6, 87.5, 0),
                "scale": (20, 0.5, 30),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(35, 55, 0),
                "scale": (10, 0.5, 10),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(45, 75, 10),
                "scale": (10, 10, 0.5),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(45, 95, -10),
                "scale": (10, 10, 0.5),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(45, 115, 10),
                "scale": (10, 10, 0.5),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(45, 135, -5),
                "scale": (10, 0.5, 10),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(87.5, 95, -5),
                "scale": (2, 2, 2),
                "diffuse": (1, 0, 0),
                "specular": (1, 0, 0),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(110, 95, -5),
                "scale": (2, 2, 2),
                "diffuse": (1, 0, 0),
                "specular": (1, 0, 0),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(135, 95, 0),
                "scale": (2, 2, 2),
                "diffuse": (1, 0, 0),
                "specular": (1, 0, 0),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(160, 95, -5),
                "scale": (2, 2, 2),
                "diffuse": (1, 0, 0),
                "specular": (1, 0, 0),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(170, 105, -30),
                "scale": (0.2, 5, 5),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(150, 135, -55),
                "scale": (0.2, 7.5, 7.5),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(170, 155, -75),
                "scale": (0.2, 7.5, 7.5),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(160, 180, -110),
                "scale": (20, 0.2, 20),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
        ]
        self.sun = CircularObject(
            sun["texture"], sun["currentpos"], sun["motion"])
        self.moon = CircularObject(
            moon["texture"], moon["currentpos"], moon["motion"])
        self.tree = Collision(self.objects)
        self.types = {
            "CUBE": Cube(),
            "SPHERE": Sphere()
        }
        self.last = None

    def add_object(self, obj):
        self.objects.push(obj)
        self.tree.add_object(obj["pos"], obj["scale"])

    def draw_orbiting_objects(self, shader, model_matrix, timer):
        ######## Setting their lights #########
        # Sun
        shader.set_sun_position(*self.sun.get_position(timer))
        shader.set_sun_diffuse(0.6, 0.6, 0.6)
        shader.set_sun_specular(0.5, 0.5, 0.5)
        shader.set_sun_ambient(0.4, 0.4, 0.4)

        # Moon
        shader.set_moon_position(*self.moon.get_position(timer))
        shader.set_moon_diffuse(0x7d / 256, 0x7f / 256, 0x83 / 256)
        shader.set_moon_specular(0x7d / 256, 0x7f / 256, 0x83 / 256)
        shader.set_moon_ambient(0x7d / 256, 0x7f / 256, 0x83 / 256)

        ######## Drawing spheres #########
        shader.set_using_texture(1.0)
        # Sun
        shader.set_diffuse_texture(self.sun.texture)
        shader.set_material_diffuse(*self.sun.diffuse)
        model_matrix.push_matrix()
        model_matrix.add_translation(*self.sun.get_position(timer))
        model_matrix.add_scale(2.5, 2.5, 2.5)
        shader.set_model_matrix(model_matrix.matrix)
        self.types["SPHERE"].draw(shader)
        model_matrix.pop_matrix()

        # Moon
        shader.set_diffuse_texture(self.moon.texture)
        shader.set_material_diffuse(*self.moon.diffuse)
        model_matrix.push_matrix()
        model_matrix.add_translation(*self.moon.get_position(timer))
        model_matrix.add_scale(2.5, 2.5, 2.5)
        shader.set_model_matrix(model_matrix.matrix)
        self.types["SPHERE"].draw(shader)
        model_matrix.pop_matrix()

        shader.set_using_texture(0.0)
        shader.set_using_specular_texture(0.0)

    def draw(self, shader, model_matrix, timer):
        self.draw_orbiting_objects(shader, model_matrix, timer)
        for item in self.objects:
            if item["texture"] is not None:
                shader.set_using_texture(1.0)
                shader.set_diffuse_texture(item["texture"])
            else:
                shader.set_using_texture(0.0)
            model_matrix.push_matrix()
            shader.set_material_diffuse(*item["diffuse"])
            model_matrix.add_translation(*item["pos"])
            model_matrix.add_scale(*item["scale"])
            shader.set_model_matrix(model_matrix.matrix)
            self.types[item["type"]].draw(shader)
            model_matrix.pop_matrix()
