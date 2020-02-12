import sys
import click
from .common import cli, cli_option
from .hittable import HittableList, Hittable
from .camera import Camera
from .sphere import Sphere
from .lambertian import Lambertian
from .metal import Metal
from .dielectric import Dielectric, Dielectric2, DielectricA, Dielectric2A
from .vec3 import Vec3
from .ray import Ray
import random
import math
from logging import getLogger

log = getLogger(__name__)


def do_main(nx, ny, ns, colorfn, world, output):
    print("P3", file=output)
    print(nx, ny, file=output)
    print(255, file=output)
    cam = Camera()
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
def metal(nx, ny, ns, output):
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.8, 0.3, 0.3))),
         Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.6, 0.0))),
         Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2))),
         Sphere(Vec3(-1, 0, -1), 0.5, Metal(Vec3(0.8, 0.8, 0.8)))])
    do_main(nx, ny, ns, color, spheres, output)


@cli.command()
@cli_option
@click.option("--fuzz", type=float, default=0.3, show_default=True)
def metal_fuzz(nx, ny, ns, fuzz, output):
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.8, 0.3, 0.3))),
         Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.6, 0.0))),
         Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), fuzz)),
         Sphere(Vec3(-1, 0, -1), 0.5, Metal(Vec3(0.8, 0.8, 0.8), fuzz))])
    do_main(nx, ny, ns, color, spheres, output)


@cli.command()
@cli_option
@click.option("--fuzz", type=float, default=0.0, show_default=True)
def metal_dielectric(nx, ny, ns, fuzz, output):
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))),
         Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0))),
         Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), fuzz)),
         Sphere(Vec3(-1, 0, -1), 0.5, Dielectric(1.5))])
    do_main(nx, ny, ns, color, spheres, output)


@cli.command()
@cli_option
@click.option("--fuzz", type=float, default=0.0, show_default=True)
def metal_dielectric_A(nx, ny, ns, fuzz, output):
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))),
         Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0))),
         Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), fuzz)),
         Sphere(Vec3(-1, 0, -1), 0.5, DielectricA(1.5))])
    do_main(nx, ny, ns, color, spheres, output)


@cli.command()
@cli_option
@click.option("--fuzz", type=float, default=0.0, show_default=True)
def metal_dielectric2(nx, ny, ns, fuzz, output):
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))),
         Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0))),
         Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), fuzz)),
         Sphere(Vec3(-1, 0, -1), 0.5, Dielectric2(1.5)),
         Sphere(Vec3(-1, 0, -1), -0.45, Dielectric2(1.5))])
    do_main(nx, ny, ns, color, spheres, output)


@cli.command()
@cli_option
@click.option("--fuzz", type=float, default=0.0, show_default=True)
def metal_dielectric2_A(nx, ny, ns, fuzz, output):
    spheres = HittableList(
        [Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))),
         Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0))),
         Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), fuzz)),
         Sphere(Vec3(-1, 0, -1), 0.5, Dielectric2A(1.5)),
         Sphere(Vec3(-1, 0, -1), -0.45, Dielectric2A(1.5))])
    do_main(nx, ny, ns, color, spheres, output)


if __name__ == "__main__":
    cli()
