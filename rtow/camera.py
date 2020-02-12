import math
from .ray import Ray
from .vec3 import Vec3


class Camera:
    def __init__(self):
        self.lower_left_corner = Vec3(-2.0, -1.0, -1.0)
        self.horizontal = Vec3(4.0, 0.0, 0.0)
        self.vertical = Vec3(0.0, 2.0, 0.0)
        self.origin = Vec3(0.0, 0.0, 0.0)

    def get_ray(self, u: float, v: float) -> Ray:
        return Ray(
            self.origin,
            self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)


class CameraPos(Camera):
    def __init__(self, vfov: float, aspect: float):
        theta = vfov * math.pi / 180
        half_height = math.tan(theta / 2)
        half_width = aspect * half_height
        self.lower_left_corner = Vec3(-half_width, -half_height, -1.0)
        self.horizontal = Vec3(2 * half_width, 0.0, 0.0)
        self.vertical = Vec3(0.0, 2 * half_height, 0.0)
        self.origin = Vec3(0.0, 0.0, 0.0)


class CameraPos2(Camera):
    def __init__(self, lookfrom: Vec3, lookat: Vec3, vup: Vec3, vfov: float, aspect: float):
        theta = vfov * math.pi / 180
        half_height = math.tan(theta / 2)
        half_width = aspect * half_height
        self.origin = lookfrom
        w = Vec3.unit_vector(lookfrom - lookat)
        u = Vec3.unit_vector(Vec3.cross(vup, w))
        v = Vec3.cross(w, u)
        self.lower_left_corner = self.origin - half_width * u - half_height * v - w
        self.horizontal = 2 * half_width * u
        self.vertical = 2 * half_height * v


class CameraBlur(Camera):
    def __init__(self, lookfrom: Vec3, lookat: Vec3, vup: Vec3, vfov: float, aspect: float, aperture: float, focus_dist: float):
        self.lens_radius = aperture / 2
        theta = vfov * math.pi / 180
        half_height = math.tan(theta / 2)
        half_width = aspect * half_height
        self.origin = lookfrom
        self.w = Vec3.unit_vector(lookfrom - lookat)
        self.u = Vec3.unit_vector(Vec3.cross(vup, self.w))
        self.v = Vec3.cross(self.w, self.u)
        self.lower_left_corner = self.origin - half_width * focus_dist * \
            self.u - half_height * focus_dist * self.v - focus_dist * self.w
        self.horizontal = 2 * half_width * focus_dist * self.u
        self.vertical = 2 * half_height * focus_dist * self.v

    def get_ray(self, s: float, t: float) -> Ray:
        rd = self.lens_radius * Vec3.random_in_unit_disk()
        offset = self.u * rd.x() + self.v * rd.y()
        return Ray(self.origin + offset, self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset)
