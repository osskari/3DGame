from aabbtree import AABB, AABBTree


class Collision:
    def __init__(self):
        self.tree = AABBTree()

    def get_aabb(self, point, bound):
        return AABB([(point.x - bound[0], point.x + bound[0]),
                     (point.y - bound[1], point.y + bound[1]),
                     (point.z - bound[2], point.z + bound[2])])

    def add_object(self, position, scale):
        self.tree.add(self.get_aabb(position, scale), position)

    def point_collision(self, point, bound):
        return self.tree.does_overlap(self.get_aabb(point, bound))

    def collision_objects(self, point, bound):
        return self.tree.overlap_values(self.get_aabb(point, bound))
