from .common import cli, cli_option
from logging import getLogger
import math

from .vec3 import Vec3
from .ray import Ray

log = getLogger(__name__)


def color1(r: Ray):
    unit_direction = Vec3.unit_vector(r.direction())
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)


def hit_sphere2(center: Vec3, radius: float, r: Ray) -> bool:
    oc = r.origin() - center
    a = Vec3.dot(r.direction(), r.direction())
    b = 2.0 * Vec3.dot(oc, r.direction())
    c = Vec3.dot(oc, oc) - radius * radius
    discriminant = b * b - 4 * a * c
    return discriminant > 0


def color2(r: Ray):
    if hit_sphere2(Vec3(0, 0, -1), 0.5, r):
        return Vec3(1, 0, 0)
    unit_direction = Vec3.unit_vector(r.direction())
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)


def hit_sphere3(center: Vec3, radius: float, r: Ray) -> bool:
    oc = r.origin() - center
    a = Vec3.dot(r.direction(), r.direction())
    b = 2.0 * Vec3.dot(oc, r.direction())
    c = Vec3.dot(oc, oc) - radius * radius
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return -1.0
    return (-b - math.sqrt(discriminant)) / (2.0 * a)


def color3(r: Ray):
    t = hit_sphere3(Vec3(0, 0, -1), 0.5, r)
    if t > 0.0:
        N = Vec3.unit_vector(r.point_at_parameter(t) - Vec3(0, 0, -1))
        return 0.5 * Vec3(N.x() + 1, N.y() + 1, N.z() + 1)
    unit_direction = Vec3.unit_vector(r.direction())
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)


def do_main(nx, ny, colorfn, output):
    print("P3", file=output)
    print(nx, ny, file=output)
    print(255, file=output)
    lower_left_corner = Vec3(-2.0, -1.0, -1.0)
    horizontal = Vec3(4.0, 0.0, 0.0)
    vertical = Vec3(0.0, 2.0, 0.0)
    origin = Vec3(0.0, 0.0, 0.0)
    for j in range(ny - 1, -1, -1):
        for i in range(nx):
            u = float(i) / float(nx)
            v = float(j) / float(ny)
            r = Ray(origin, lower_left_corner + u * horizontal + v * vertical)
            col = colorfn(r)
            ir = int(255.99 * col[0])
            ig = int(255.99 * col[1])
            ib = int(255.99 * col[2])
            print(ir, ig, ib, file=output)


@cli.command()
@cli_option
def blue(nx, ny, ns, output):
    do_main(nx, ny, color1, output)


@cli.command()
@cli_option
def sphere(nx, ny, ns, output):
    do_main(nx, ny, color2, output)


@cli.command()
@cli_option
def sphere2(nx, ny, ns, output):
    do_main(nx, ny, color3, output)


if __name__ == "__main__":
    cli()
