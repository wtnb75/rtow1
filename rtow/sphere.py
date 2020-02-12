from typing import Tuple
import math
from .vec3 import Vec3
from .ray import Ray
from .hittable import Hittable, HitRecord, Material


class Sphere(Hittable):
    def __init__(self, cen: Vec3 = None, radius: float = 0.0, material: Material = None):
        if cen is not None:
            self.center = cen
        else:
            self.center = Vec3()
        self.radius = radius
        self.material = material

    def hit(self, r: Ray, t_min: float, t_max: float) -> Tuple[bool, HitRecord]:
        oc = r.origin() - self.center
        a = Vec3.dot(r.direction(), r.direction())
        b = Vec3.dot(oc, r.direction())
        c = Vec3.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - a * c
        if discriminant > 0:
            temp = (-b - math.sqrt(discriminant)) / a
            if temp < t_max and temp > t_min:
                rec = HitRecord()
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                rec.material = self.material
                return True, rec
            temp = (-b + math.sqrt(discriminant)) / a
            if temp < t_max and temp > t_min:
                rec = HitRecord()
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                rec.material = self.material
                return True, rec
        return False, None
