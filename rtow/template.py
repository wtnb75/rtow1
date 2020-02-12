from .common import cli, cli_option
from logging import getLogger

log = getLogger(__name__)


@cli.command()
@cli_option
def hello(nx, ny, ns, output):
    log.info("nx=%d, ny=%d, ns=%d", nx, ny, ns)


if __name__ == "__main__":
    cli()
