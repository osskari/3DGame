from aabbtree import AABB, AABBTree
from Base3DObjects import Point, Vector


# Object that helps with collision detection using the AABBTree object
class Collision:
    def __init__(self, objects=None):
        self.tree = AABBTree()
        if objects:
            for item in objects:
                self.add_object(item["pos"], item["scale"])

    # Returns AABB object with coorect values based on a point and offset
    def get_aabb(self, point, bound):
        return AABB([(point.x - bound[0], point.x + bound[0]),
                     (point.y - bound[1], point.y + bound[1]),
                     (point.z - bound[2], point.z + bound[2])])

    # Add object with position and scale to the tree
    # Sets the position as the value returned in case of collision
    def add_object(self, position, scale):
        print(self.get_aabb(position, scale))
        self.tree.add(self.get_aabb(position, scale),
                      {"pos": position, "scale": scale})

    # Makes checking for collision on point easier
    def point_collision(self, point, bound):
        return self.tree.does_overlap(self.get_aabb(point, bound))

    # Returns the point object of collided objects
    def collision_objects(self, point, bound):
        return self.tree.overlap_values(self.get_aabb(point, bound))

    # checks if player is between bounds of object on an axis with respect to size of both
    def is_between(self, player, obj, axis):
        return obj["pos"][axis] - obj["scale"][axis] < player["pos"][axis] < obj["pos"][axis] + obj["scale"][axis]

    # Finds which side of a cube the player is touching
    def get_colliding_face(self, player, obj):
        # Zeroes the axis of the plane on the object the player is touching
        return (1 if self.is_between(player, obj, 0) else 0,
                1 if self.is_between(player, obj, 1) else 0,
                1 if self.is_between(player, obj, 2) else 0)

    # Returns surface vector based on player direction
    def get_surface_vector(self, player, obj):
        directions = self.get_colliding_face(player, obj)
        # Returns a normalized vector that represents the direction of the surface
        # Direction on the non zeroed axes based on player movement
        return Vector(player["direction"].x * directions[0], player["direction"].y * directions[1], player["direction"].z * directions[2]).normalize()

    # Returns slide vector for player on collided object
    def get_slide_vector(self, player, obj):
        surface_vector = self.get_surface_vector(player, obj)
        return surface_vector * player["direction"].dot(surface_vector)

    # Returns motion vector of player
    def move(self, player):
        # collision member set to advoid key error
        player["collision"] = []
        # If no collision return player directly
        if(not self.point_collision(player["newpos"], player["scale"])):
            return player
        else:
            # If collision, get slide vector for each object collided with
            print("player aabb:", player["pos"])
            a = self.collision_objects(player["newpos"], player["scale"])
            for i in a:
                print(self.get_aabb(i["pos"], i["scale"]))
            for item in self.collision_objects(player["newpos"], player["scale"]):
                player["direction"] = self.get_slide_vector(player, item)
                player["collision"].append(
                    self.get_colliding_face(player, item))
            return player


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
