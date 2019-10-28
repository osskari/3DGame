from aabbtree import AABB, AABBTree
from Base3DObjects import Vector

# Object that helps with collision detection using the AABBTree object


class Collision:
    def __init__(self):
        self.tree = AABBTree()

    # Returns AABB object with coorect values based on a point and offset
    def get_aabb(self, point, bound):
        return AABB([(point.x - bound[0], point.x + bound[0]),
                     (point.y - bound[1], point.y + bound[1]),
                     (point.z - bound[2], point.z + bound[2])])

    # Add object with position and scale to the tree
    # Sets the position as the value returned in case of collision
    def add_object(self, position, scale):
        self.tree.add(self.get_aabb(position, scale),
                      {"pos": position, "scale": scale})

    # Makes checking for collision on point easier
    def point_collision(self, point, bound):
        return self.tree.does_overlap(self.get_aabb(point, bound))

    # Returns the point object of collided objects
    def collision_objects(self, point, bound):
        return self.tree.overlap_values(self.get_aabb(point, bound))

    def is_between(self, player, object, axis):
        num = (0 if axis == "x" else 1 if axis == "y" else 2)
        return object["pos"][num] - object["scale"][num] - player["scale"][num] < player["pos"][num] < object["pos"][num] + object["scale"][num] + player["scale"][num]

    def get_colliding_face(self, player, obj):
        if (self.is_between(player, obj, "x")) and (self.is_between(player, obj, "z")):
            if obj["pos"].y < player["pos"].y:
                print("top")
                return Vector(player["direction"].x, 0, player["direction"].z).normalize()
            else:
                print("bottom")
                return Vector(player["direction"].x, 0, player["direction"].z).normalize()

        if (self.is_between(player, obj, "x")) and (self.is_between(player, obj, "y")):
            if obj["pos"].z < player["pos"].z:
                print("north")
                return Vector(player["direction"].x, player["direction"].y, 0).normalize()
            else:
                print("south")
                return Vector(player["direction"].x, player["direction"].y, 0).normalize()

        if (self.is_between(player, obj, "y")) and (self.is_between(player, obj, "z")):
            if obj["pos"].x < player["pos"].x:
                print("east")
                return Vector(0, player["direction"].y, player["direction"].z).normalize()
            else:
                print("west")
                return Vector(0, player["direction"].y, player["direction"].z).normalize()

    def get_slide_vector(self, player, obj):
        surface_vector = self.get_colliding_face(player, obj)
        return surface_vector * player["direction"].dot(surface_vector)
