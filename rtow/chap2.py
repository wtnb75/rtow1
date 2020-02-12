from .common import cli, cli_option
from logging import getLogger
from .vec3 import Vec3

log = getLogger(__name__)


@cli.command()
@cli_option
def output_image(nx, ny, ns, output):
    print("P3", file=output)
    print(nx, ny, file=output)
    print(255, file=output)
    for j in range(ny - 1, -1, -1):
        for i in range(nx):
            r = float(i) / float(nx)
            g = float(j) / float(ny)
            b = 0.2
            ir = int(255.99 * r)
            ig = int(255.99 * g)
            ib = int(255.99 * b)
            print(ir, ig, ib, file=output)


@cli.command()
@cli_option
def output_image_vec3(nx, ny, ns, output):
    print("P3", file=output)
    print(nx, ny, file=output)
    print(255, file=output)
    for j in range(ny - 1, -1, -1):
        for i in range(nx):
            col = Vec3(float(i) / float(nx), float(j) / float(ny), 0.2)
            ir = int(255.99 * col[0])
            ig = int(255.99 * col[1])
            ib = int(255.99 * col[2])
            print(ir, ig, ib, file=output)


if __name__ == "__main__":
    cli()
