class CircularObject:
    def __init__(self, texture_id, position, motion=None):
        self.diffuse = (0.5, 0.5, 0.5)
        self.specular = (0.5, 0.5, 0.5)
        self.shininess = 1
        self.texture = texture_id
        self.position = position
        self.bezier_motion = motion

    def get_position(self, time=None):
        if time is None or self.bezier_motion is None:
            return self.position
        else:
            return self.bezier_motion.get_current_position(time)

    def restart_motion(self, time):
        self.bezier_motion.restart(time, 40)

    def bezier_done(self, time):
        if time > self.bezier_motion.end_time:
            return True
        return False
