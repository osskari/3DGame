from aabbtree import AABB, AABBTree
from Base3DObjects import Point, Vector


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
        return object["pos"][num] - object["scale"][num] - player["scale"][num] < player["pos"][num] < object["pos"][
            num] + object["scale"][num] + player["scale"][num]

    def get_colliding_face(self, player, obj):
        if (self.is_between(player, obj, "x")) and (self.is_between(player, obj, "z")):
            if obj["pos"].y < player["pos"].y:
                print("top")
                return Vector(0.0, 0.0, 0.0)
            else:
                print("bottom")

        if (self.is_between(player, obj, "x")) and (self.is_between(player, obj, "y")):
            if obj["pos"].z < player["pos"].z:
                print("north")
            else:
                print("south")

        if (self.is_between(player, obj, "y")) and (self.is_between(player, obj, "z")):
            if obj["pos"].x < player["pos"].x:
                print("east")
            else:
                print("west")


class BezierMotion:
    def __init__(self, start_time, end_time, *bezier_points):
        self.points = []
        for point in bezier_points:
            self.points.append(point)
        self.start_time = start_time
        self.end_time = end_time

    def get_current_position(self, time):
        t = (time - self.start_time) / (self.end_time - self.start_time)
        if time < self.start_time:
            return self.points[0]
        elif time > self.end_time:
            return self.points[len(self.points) - 1]
        else:
            return self._rec_pos(t, self.points)

    def _rec_pos(self, t, point_list):
        if len(point_list) == 1:
            return point_list[0]
        temp_list = []
        for i in range(len(point_list) - 1):
            temp_list.append(
                point_list[i] * (1.0 - t) + point_list[i + 1] * t
            )
        return self._rec_pos(t, temp_list)

    def restart(self, now, time):
        self.start_time = now
        self.end_time = now + time
