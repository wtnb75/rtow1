import math
import array
import random


class Vec3:
    def __init__(self, e0: float = 0.0, e1: float = 0.0, e2: float = 0.0):
        self.e = array.array('f', [e0, e1, e2])

    def x(self): return self.e[0]
    def y(self): return self.e[1]
    def z(self): return self.e[2]
    def r(self): return self.e[0]
    def g(self): return self.e[1]
    def b(self): return self.e[2]
    def __pos__(self): return self

    def __neg__(self): return Vec3(-self.e[0], -self.e[1], -self.e[2])
    def __getitem__(self, i: int): return self.e[i]

    def __add__(self, v):
        return Vec3(self.e[0] + v.e[0], self.e[1] + v.e[1], self.e[2] + v.e[2])

    def __sub__(self, v):
        return Vec3(self.e[0] - v.e[0], self.e[1] - v.e[1], self.e[2] - v.e[2])

    def __mul__(self, v):
        if isinstance(v, Vec3):
            return Vec3(self.e[0] * v.e[0], self.e[1] * v.e[1], self.e[2] * v.e[2])
        elif isinstance(v, (float, int)):
            return Vec3(self.e[0] * v, self.e[1] * v, self.e[2] * v)
        raise Exception("type mismatch")

    def __rmul__(self, v):
        if isinstance(v, Vec3):
            return Vec3(self.e[0] * v.e[0], self.e[1] * v.e[1], self.e[2] * v.e[2])
        elif isinstance(v, (float, int)):
            return Vec3(self.e[0] * v, self.e[1] * v, self.e[2] * v)
        raise Exception("type mismatch")

    def __truediv__(self, v):
        if isinstance(v, Vec3):
            return Vec3(self.e[0] / v.e[0], self.e[1] / v.e[1], self.e[2] / v.e[2])
        elif isinstance(v, (float, int)):
            return Vec3(self.e[0] / v, self.e[1] / v, self.e[2] / v)
        raise Exception("type mismatch")

    def __rtruediv__(self, v):
        if isinstance(v, Vec3):
            return Vec3(self.e[0] / v.e[0], self.e[1] / v.e[1], self.e[2] / v.e[2])
        elif isinstance(v, (float, int)):
            return Vec3(self.e[0] / v, self.e[1] / v, self.e[2] / v)
        raise Exception("type mismatch")

    def length(self):
        return math.sqrt(self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2])

    def squared_length(self):
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]

    def make_unit_vector(self):
        k = 1.0 / math.sqrt(self.e[0] * self.e[0] +
                            self.e[1] * self.e[1] + self.e[2] * self.e[2])
        self.e[0] *= k
        self.e[1] *= k
        self.e[2] *= k

    def __str__(self):
        return "{} {} {}".format(self.e[0], self.e[1], self.e[2])

    def __iadd__(self, v):
        if isinstance(v, Vec3):
            self.e[0] += v.e[0]
            self.e[1] += v.e[1]
            self.e[2] += v.e[2]
            return self
        elif isinstance(v, (float, int)):
            self.e[0] += v
            self.e[1] += v
            self.e[2] += v
            return self
        raise Exception("type mismatch")

    def __isub__(self, v):
        if isinstance(v, Vec3):
            self.e[0] -= v.e[0]
            self.e[1] -= v.e[1]
            self.e[2] -= v.e[2]
            return self
        elif isinstance(v, (float, int)):
            self.e[0] -= v
            self.e[1] -= v
            self.e[2] -= v
            return self
        raise Exception("type mismatch")

    def __imul__(self, v):
        if isinstance(v, Vec3):
            self.e[0] *= v.e[0]
            self.e[1] *= v.e[1]
            self.e[2] *= v.e[2]
            return self
        elif isinstance(v, (float, int)):
            self.e[0] *= v
            self.e[1] *= v
            self.e[2] *= v
            return self
        raise Exception("type mismatch")

    def __itruediv__(self, v):
        if isinstance(v, Vec3):
            self.e[0] /= v.e[0]
            self.e[1] /= v.e[1]
            self.e[2] /= v.e[2]
            return self
        elif isinstance(v, (float, int)):
            self.e[0] /= v
            self.e[1] /= v
            self.e[2] /= v
            return self
        raise Exception("type mismatch")

    @classmethod
    def unit_vector(cls, v):
        return v / v.length()

    @classmethod
    def dot(cls, v1, v2):
        return v1.e[0] * v2.e[0] + v1.e[1] * v2.e[1] + v1.e[2] * v2.e[2]

    @classmethod
    def cross(cls, v1, v2):
        return Vec3(v1.e[1] * v2.e[2] - v1.e[2] * v2.e[1],
                    v1.e[2] * v2.e[0] - v1.e[0] * v2.e[2],
                    v1.e[0] * v2.e[1] - v1.e[1] * v2.e[0])

    @classmethod
    def random_in_unit_sphere(cls):
        while True:
            p = 2.0 * Vec3(random.random(), random.random(),
                           random.random()) - Vec3(1, 1, 1)
            if p.squared_length() < 1.0:
                return p

    @classmethod
    def random_in_unit_disk(cls):
        while True:
            p = 2.0 * Vec3(random.random(), random.random(), 0) - Vec3(1, 1, 0)
            if cls.dot(p, p) < 1.0:
                return p
