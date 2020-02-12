import math
import random
from typing import Tuple
from .ray import Ray
from .vec3 import Vec3
from .hittable import Material, HitRecord
from .metal import Metal


class Dielectric(Material):
    def __init__(self, ri: float):
        self.ref_idx = ri

    @classmethod
    def refract(cls, v: Vec3, n: Vec3, ni_over_nt: float) -> Tuple[bool, Vec3]:
        uv = Vec3.unit_vector(v)
        dt = Vec3.dot(uv, n)
        discriminant = 1.0 - ni_over_nt * ni_over_nt * (1.0 - dt * dt)
        if discriminant > 0:
            return True, ni_over_nt * (uv - n * dt) - n * math.sqrt(discriminant)
        return False, None

    def scatter(self, ray: Ray, rec: HitRecord) -> Tuple[bool, Ray, Vec3]:
        reflected = Metal.reflect(ray.direction(), rec.normal)
        attenuation = Vec3(1.0, 1.0, 0.0)  # BUG
        if Vec3.dot(ray.direction(), rec.normal) > 0:
            outward_normal = -rec.normal
            ni_over_nt = self.ref_idx
        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0 / self.ref_idx
        flg, refracted = self.refract(
            ray.direction(), outward_normal, ni_over_nt)
        if flg:
            scattered = Ray(rec.p, refracted)
            return True, scattered, attenuation
        scattered = Ray(rec.p, reflected)
        return False, scattered, attenuation


class DielectricA(Dielectric):
    def scatter(self, ray: Ray, rec: HitRecord) -> Tuple[bool, Ray, Vec3]:
        res = super().scatter(ray, rec)
        # BugFix (attenuation = Vec3(1.0, 1.0, 1.0))
        return res[0], res[1], Vec3(1.0, 1.0, 1.0)


class Dielectric2(Material):
    def __init__(self, ri: float):
        self.ref_idx = ri

    @classmethod
    def schlick(cls, cosine: float, ref_idx: float):
        r0 = (1.0 - ref_idx) / (1.0 + ref_idx)
        r0 = r0 * r0
        return r0 + (1.0 - r0) * math.pow((1.0 - cosine), 5)

    def scatter(self, ray: Ray, rec: HitRecord) -> Tuple[bool, Ray, Vec3]:
        reflected = Metal.reflect(ray.direction(), rec.normal)
        attenuation = Vec3(1.0, 1.0, 0.0)  # BUG
        if Vec3.dot(ray.direction(), rec.normal) > 0:
            outward_normal = -rec.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * \
                Vec3.dot(ray.direction(), rec.normal) / \
                ray.direction().length()
        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0 / self.ref_idx
            cosine = -Vec3.dot(ray.direction(), rec.normal) / \
                ray.direction().length()
        flg, refracted = Dielectric.refract(
            ray.direction(), outward_normal, ni_over_nt)
        if flg:
            reflect_prob = self.schlick(cosine, self.ref_idx)
        else:
            reflect_prob = 1.0
        if random.random() < reflect_prob:
            scattered = Ray(rec.p, reflected)
        else:
            scattered = Ray(rec.p, refracted)
        return True, scattered, attenuation


class Dielectric2A(Dielectric2):
    def scatter(self, ray: Ray, rec: HitRecord) -> Tuple[bool, Ray, Vec3]:
        res = super().scatter(ray, rec)
        # BugFix (attenuation = Vec3(1.0, 1.0, 1.0))
        return res[0], res[1], Vec3(1.0, 1.0, 1.0)
