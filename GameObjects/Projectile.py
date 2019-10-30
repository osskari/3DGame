from HelperObjects import BezierMotion
from Base3DObjects import Vector, Point

class Projectile:
    def __init__(self, eye_pos, n_vec, time):
        sine = 1 - n_vec.normalize().dot(Vector(0,1,0))
        n_vec = (n_vec * -1) * sine
        self.motion = BezierMotion(
            time,
            time + (2 * sine),
            eye_pos,
            eye_pos + n_vec,
            Point(eye_pos.x + ( (n_vec.x + n_vec.x) * 4), 0, eye_pos.z + ( (n_vec.z + n_vec.z) * 4)))
        
        

    def get_current_position(self, time):
        return self.motion.get_current_position(time)