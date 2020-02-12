import sys
import random
import math
import click
from .vec3 import Vec3
from .camera import CameraPos, CameraPos2, CameraBlur
from .common import cli, cli_option
from .hittable import HittableList, Hittable
from .sphere import Sphere
from .lambertian import Lambertian
from .metal import Metal
from .dielectric import Dielectric2A
from .ray import Ray
from logging import getLogger

log = getLogger(__name__)


def do_main(nx, ny, ns, colorfn, world, cam, output):
    print("P3", file=output)
    print(nx, ny, file=output)
    print(255, file=output)
    with click.progressbar(range(ny - 1, -1, -1), length=ny, file=sys.stderr) as bar:
        for j in bar:
            for i in range(nx):
                col = Vec3(0, 0, 0)
                for s in range(ns):
                    u = float(i + random.random()) / float(nx)
                    v = float(j + random.random()) / float(ny)
                    r = cam.get_ray(u, v)
                    col += colorfn(r, world, 0)
                col /= float(ns)
                col = Vec3(math.sqrt(col[0]), math.sqrt(
                    col[1]), math.sqrt(col[2]))
                ir = int(255.99 * col[0])
                ig = int(255.99 * col[1])
                ib = int(255.99 * col[2])
                print(ir, ig, ib, file=output)


def color(r: Ray, world: Hittable, depth: int) -> Vec3:
    flg, rec = world.hit(r, 0.001, sys.float_info.max)
    if flg:
        flg2, scattered, attenuation = rec.material.scatter(r, rec)
        if depth < 50 and flg2:
            return attenuation * color(scattered, world, depth + 1)
        return Vec3(0, 0, 0)
    unit_direction = Vec3.unit_vector(r.direction())
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)


@cli.command()
@cli_option
def camera_pos(nx, ny, ns, output):
    cam = CameraPos(90, float(nx) / float(ny))
    R = math.cos(math.pi / 4)
    spheres = HittableList(
        [Sphere(Vec3(-R, 0, -1), R, Lambertian(Vec3(0, 0, 1))),
         Sphere(Vec3(R, 0, -1), R, Lambertian(Vec3(1, 0, 0)))])
    do_main(nx, ny, ns, color, spheres, cam, output)


@cli.command()
@cli_option
@click.option("--fuzz", type=float, default=0.0, show_default=True)
def camera_pos2(nx, ny, ns, fuzz, output):
    cam = CameraPos2(Vec3(-2, 2, 1), Vec3(0, 0, -1),
                     Vec3(0, 1, 0), 90, float(nx) / float(ny))
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))),
         Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0))),
         Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), fuzz)),
         Sphere(Vec3(-1, 0, -1), 0.5, Dielectric2A(1.5)),
         Sphere(Vec3(-1, 0, -1), -0.45, Dielectric2A(1.5))])
    do_main(nx, ny, ns, color, spheres, cam, output)


@cli.command()
@cli_option
@click.option("--fuzz", type=float, default=0.0, show_default=True)
def camera_pos2_2(nx, ny, ns, fuzz, output):
    cam = CameraPos2(Vec3(-1, 1, 1), Vec3(0, 0, -1),
                     Vec3(0, 1, 0), 90, float(nx) / float(ny))
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))),
         Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0))),
         Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), fuzz)),
         Sphere(Vec3(-1, 0, -1), 0.5, Dielectric2A(1.5)),
         Sphere(Vec3(-1, 0, -1), -0.45, Dielectric2A(1.5))])
    do_main(nx, ny, ns, color, spheres, cam, output)


@cli.command()
@cli_option
@click.option("--fuzz", type=float, default=0.0, show_default=True)
def camera_blur(nx, ny, ns, fuzz, output):
    lookfrom = Vec3(3, 3, 2)
    lookat = Vec3(0, 0, -1)
    dist_to_focus = (lookfrom - lookat).length()
    aperture = 2.0
    cam = CameraBlur(lookfrom, lookat, Vec3(0, 1, 0), 20,
                     float(nx) / float(ny), aperture, dist_to_focus)
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))),
         Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0))),
         Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), fuzz)),
         Sphere(Vec3(-1, 0, -1), 0.5, Dielectric2A(1.5)),
         Sphere(Vec3(-1, 0, -1), -0.45, Dielectric2A(1.5))])
    do_main(nx, ny, ns, color, spheres, cam, output)


if __name__ == "__main__":
    cli()
