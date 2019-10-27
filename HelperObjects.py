from aabbtree import AABB, AABBTree

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
        self.tree.add(self.get_aabb(position, scale), position)

    # Makes checking for collision on point easier
    def point_collision(self, point, bound):
        return self.tree.does_overlap(self.get_aabb(point, bound))

    # Returns the point object of collided objects
    def collision_objects(self, point, bound):
        return self.tree.overlap_values(self.get_aabb(point, bound))
