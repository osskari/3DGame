from aabbtree import AABB, AABBTree
from Base3DObjects import Point
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

class BazierMotion:
    def __init__(self, start_time, end_time, *bazier_points):
        self.points = []
        for point in bazier_points:
            self.points.append(point)
        self.start_time = start_time
        self.end_time = end_time

    def get_current_position(self, time):
        t = (time - self.start_time) / (self.end_time - self.start_time)
        if(time < self.start_time):
            return self.points[0]
        elif (time > self.end_time):
            return self.points[len(self.points) - 1]
        else:
            return self._rec_pos(t, self.points)
            
    def _rec_pos(self, t, point_list):
        if(len(point_list) == 1):
            return point_list[0]
        templist = []
        for i in range(len(point_list) - 1):
            templist.append(
                point_list[i] * (1.0 - t)  +  point_list[i+1] * t
            )
        return self._rec_pos(t, templist)



        