from .camera import Camera
from .sphere import Sphere
from .hittable import Hittable, HitRecord, HittableList
from .ray import Ray
from .vec3 import Vec3
import sys
import math
import random

from .common import cli, cli_option
from logging import getLogger

log = getLogger(__name__)


def color(r: Ray, world: Hittable) -> Vec3:
    rec = HitRecord()
    flg, rec = world.hit(r, 0.0, sys.float_info.max)
    if flg:
        return 0.5 * Vec3(rec.normal.x() + 1, rec.normal.y() + 1, rec.normal.z() + 1)
    unit_direction = Vec3.unit_vector(r.direction())
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)


@cli.command()
@cli_option
def sphere_multi(nx, ny, ns, output):
    print("P3", file=output)
    print(nx, ny, file=output)
    print(255, file=output)
    lower_left_corner = Vec3(-2.0, -1.0, -1.0)
    horizontal = Vec3(4.0, 0.0, 0.0)
    vertical = Vec3(0.0, 2.0, 0.0)
    origin = Vec3(0.0, 0.0, 0.0)
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5), Sphere(Vec3(0, -100.5, -1), 100)])
    for j in range(ny - 1, -1, -1):
        for i in range(nx):
            u = float(i) / float(nx)
            v = float(j) / float(ny)
            r = Ray(origin, lower_left_corner + u * horizontal + v * vertical)
            # p = r.point_at_parameter(2.0)
            col = color(r, spheres)
            ir = int(255.99 * col[0])
            ig = int(255.99 * col[1])
            ib = int(255.99 * col[2])
            print(ir, ig, ib, file=output)


def do_main_aa(nx, ny, ns, colorfn, output):
    print("P3", file=output)
    print(nx, ny, file=output)
    print(255, file=output)
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5), Sphere(Vec3(0, -100.5, -1), 100)])
    cam = Camera()
    for j in range(ny - 1, -1, -1):
        for i in range(nx):
            col = Vec3(0, 0, 0)
            for s in range(ns):
                u = float(i + random.random()) / float(nx)
                v = float(j + random.random()) / float(ny)
                r = cam.get_ray(u, v)
                col += colorfn(r, spheres)
            col /= float(ns)
            ir = int(255.99 * col[0])
            ig = int(255.99 * col[1])
            ib = int(255.99 * col[2])
            print(ir, ig, ib, file=output)


@cli.command()
@cli_option
def antialias(nx, ny, ns, output):
    do_main_aa(nx, ny, ns, color, output)


def color2(r: Ray, world: Hittable) -> Vec3:
    flg, rec = world.hit(r, 0.001, sys.float_info.max)
    if flg:
        rnd = Vec3.random_in_unit_sphere()
        target = rec.p + rec.normal + rnd
        log.debug("hit target=%s, r=%s, rec=%s, rnd=%s", target, r, rec, rnd)
        return 0.5 * color2(Ray(rec.p, target - rec.p), world)
    unit_direction = Vec3.unit_vector(r.direction())
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)


@cli.command()
@cli_option
def diffuse(nx, ny, ns, output):
    do_main_aa(nx, ny, ns, color2, output)


def do_main_glay(nx, ny, ns, colorfn, output):
    print("P3", file=output)
    print(nx, ny, file=output)
    print(255, file=output)
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5), Sphere(Vec3(0, -100.5, -1), 100)])
    cam = Camera()
    for j in range(ny - 1, -1, -1):
        for i in range(nx):
            col = Vec3(0, 0, 0)
            for s in range(ns):
                u = float(i + random.random()) / float(nx)
                v = float(j + random.random()) / float(ny)
                r = cam.get_ray(u, v)
                col += colorfn(r, spheres)
            col /= float(ns)
            col = Vec3(math.sqrt(col[0]), math.sqrt(col[1]), math.sqrt(col[2]))
            ir = int(255.99 * col[0])
            ig = int(255.99 * col[1])
            ib = int(255.99 * col[2])
            print(ir, ig, ib, file=output)


@cli.command()
@cli_option
def diffuse_glay(nx, ny, ns, output):
    do_main_glay(nx, ny, ns, color2, output)


if __name__ == "__main__":
    cli()
