from typing import Tuple
from .ray import Ray
from .vec3 import Vec3
from .hittable import Material, HitRecord


class Lambertian(Material):
    def __init__(self, a: Vec3):
        self.albedo = a

    def scatter(self, ray: Ray, rec: HitRecord) -> Tuple[bool, Ray, Vec3]:
        target = rec.p + rec.normal + Vec3.random_in_unit_sphere()
        scattered = Ray(rec.p, target - rec.p)
        return True, scattered, self.albedo
