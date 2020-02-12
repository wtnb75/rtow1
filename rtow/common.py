import sys
import time
import functools
from logging import getLogger, basicConfig, INFO, DEBUG
import click
from .version import VERSION

log = getLogger(__name__)


@click.version_option(version=VERSION, prog_name="rtow")
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


def set_verbose(flag):
    fmt = '%(asctime)s %(levelname)s %(message)s'
    if flag:
        basicConfig(level=DEBUG, format=fmt)
    else:
        basicConfig(level=INFO, format=fmt)


_cli_option = [
    click.option("--verbose/--no-verbose"),
    click.option("--xsize", "nx", type=int, default=200, show_default=True),
    click.option("--ysize", "ny", type=int, default=100, show_default=True),
    click.option("--ns", type=int, default=100, show_default=True),
    click.argument("output", type=click.File('w'), default=sys.stdout),
]


def multi_options(decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


def cli_option(func):
    @functools.wraps(func)
    def wrap(verbose, nx, ny, ns, *args, **kwargs):
        set_verbose(verbose)
        log.info("func=%s, nx=%d, ny=%d, ns=%d", func.__name__, nx, ny, ns)
        ts = time.time()
        res = func(nx=nx, ny=ny, ns=ns, *args, **kwargs)
        log.info("render time: %f", time.time() - ts)
        return res
    return multi_options(_cli_option)(wrap)
