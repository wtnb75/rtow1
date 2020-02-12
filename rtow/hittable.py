from typing import List, Tuple
from .vec3 import Vec3
from .ray import Ray


class HitRecord:
    def __init__(self):
        self.t = 0.0
        self.p = Vec3()
        self.normal = Vec3()
        self.material = None

    def __str__(self) -> str:
        return "t=%s, p=%s, normal=%s, material=%s" % (self.t, self.p, self.normal, self.material)


class Material:
    def scatter(self, ray: Ray, rec: HitRecord) -> Tuple[bool, Ray, Vec3]:
        raise NotImplementedError("not implemented")


class Hittable:
    def hit(self, ray: Ray, t_min: float, t_max: float) -> Tuple[bool, HitRecord]:
        raise NotImplementedError("hit")


class HittableList(Hittable):
    def __init__(self, lst: List[Hittable] = []):
        self.lst = list(lst)

    def hit(self, ray: Ray, t_min: float, t_max: float) -> Tuple[bool, HitRecord]:
        rec = None
        hit_anything = False
        closest_so_far = t_max
        for i in self.lst:
            flg, temp_rec = i.hit(ray, t_min, closest_so_far)
            if flg:
                rec = temp_rec
                hit_anything = True
                closest_so_far = temp_rec.t
        return hit_anything, rec
