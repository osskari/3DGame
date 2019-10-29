from HelperObjects import Collision
from Base3DObjects import Point, OptimizedCube as Cube, OptimizedSphere as Sphere


class Map:
    def __init__(self):
        self.objects = [
            {
                "pos": Point(0, 0, 0),
                "scale": (30, 0.5, 30),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            },
            {
                "pos": Point(0, 10, 0),
                "scale": (10, 0.5, 10),
                "diffuse": (1, 1, 1),
                "specular": (1, 1, 1),
                "shininess": 13,
                "type": "CUBE",
                "texture": 1
            }
        ]
        self.tree = Collision(self.objects)
        self.types = {
            "CUBE": Cube(),
            "SPHERE": Sphere()
        }
        self.last = None

    def add_object(self, obj):
        self.objects.push(obj)
        self.tree.add_object(obj["pos"], obj["scale"])

    def draw(self, shader, model_matrix):
        for item in self.objects:
            if not self.last or not self.last == item["type"]:
                self.types[item["type"]].set_vertices(shader)
            if item["texture"] is not None:
                shader.set_using_texture(1.0)
            else:
                shader.set_using_texture(0.0)
            shader.set_diffuse_texture(item["texture"])
            model_matrix.push_matrix()
            shader.set_material_diffuse(*item["diffuse"])
            model_matrix.add_translation(*item["pos"])
            model_matrix.add_scale(*item["scale"])
            shader.set_model_matrix(model_matrix.matrix)
            self.types[item["type"]].draw(shader)
            model_matrix.pop_matrix()
