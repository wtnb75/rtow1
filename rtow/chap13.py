import sys
import random
import math
import click
from .vec3 import Vec3
from .camera import CameraBlur
from .common import cli, cli_option
from .hittable import HittableList, Hittable
from .sphere import Sphere
from .lambertian import Lambertian
from .metal import Metal
from .dielectric import DielectricA
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
@click.option("--fuzz", type=float, default=0.0, show_default=True)
@click.option("--step", type=int, default=1, show_default=True)
def where_next(nx, ny, ns, fuzz, step, output):
    lookfrom = Vec3(13, 2, 3)
    lookat = Vec3(0, 0, 0)
    # dist_to_focus = (lookfrom - lookat).length()
    dist_to_focus = 10.0
    aperture = 0.1
    cam = CameraBlur(lookfrom, lookat, Vec3(0, 1, 0), 20,
                     float(nx) / float(ny), aperture, dist_to_focus)
    # ground
    htlist = [Sphere(Vec3(0, -1000, 0), 1000, Lambertian(Vec3(0.5, 0.5, 0.5)))]
    # random balls
    for a in range(-11, 11, step):
        for b in range(-11, 11, step):
            choose_mat = random.random()
            center = Vec3(a + 0.9 * random.random(),
                          0.2, b + 0.9 * random.random())
            if (center - Vec3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    v = Vec3(random.random() * random.random(),
                             random.random() * random.random(),
                             random.random() * random.random())
                    htlist.append(Sphere(center, 0.2, Lambertian(v)))
                elif choose_mat < 0.95:
                    # metal
                    v = Vec3(0.5 * (1 + random.random()),
                             0.5 * (1 + random.random()),
                             0.5 * (1 + random.random()))
                    htlist.append(
                        Sphere(center, 0.2, Metal(v, 0.5 * random.random())))
                else:
                    # glass
                    htlist.append(Sphere(center, 0.2, DielectricA(1.5)))
    # main 3 sphere
    htlist.append(Sphere(Vec3(0, 1, 0), 1.0, DielectricA(1.5)))
    htlist.append(Sphere(Vec3(-4, 1, 0), 1.0, Lambertian(Vec3(0.4, 0.2, 0.2))))
    htlist.append(Sphere(Vec3(4, 1, 0), 1.0, Metal(Vec3(0.7, 0.6, 0.5))))
    world = HittableList(htlist)
    do_main(nx, ny, ns, color, world, cam, output)


if __name__ == "__main__":
    cli()
