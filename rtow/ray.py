
from .vec3 import Vec3


class Ray:
    def __init__(self, a: Vec3, b: Vec3):
        self.a, self.b = a, b

    def origin(self):
        return self.a

    def direction(self):
        return self.b

    def point_at_parameter(self, t: float):
        return self.a + t * self.b

    def __str__(self) -> str:
        return "a=%s, b=%s" % (self.a, self.b)
