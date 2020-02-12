from typing import Tuple
from .ray import Ray
from .vec3 import Vec3
from .hittable import Material, HitRecord


class Metal(Material):
    def __init__(self, a: Vec3, fuzz: float = 0.0):
        self.albedo = a
        if fuzz < 1.0:
            self.fuzz = fuzz
        else:
            self.fuzz = 1.0

    @classmethod
    def reflect(cls, v: Vec3, n: Vec3) -> Vec3:
        return v - 2 * Vec3.dot(v, n) * n

    def scatter(self, ray: Ray, rec: HitRecord) -> Tuple[bool, Ray, Vec3]:
        reflected = self.reflect(Vec3.unit_vector(ray.direction()), rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz *
                        Vec3.random_in_unit_sphere())
        attenuation = self.albedo
        res = (Vec3.dot(scattered.direction(), rec.normal) > 0)
        return res, scattered, attenuation
