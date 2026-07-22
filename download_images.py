# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "click",
#   "scipy",
#   "tqdm",
#   "torchvision",
# ]
# ///

from pathlib import Path

import click
from torchvision.datasets import Flowers102


@click.command()
@click.option(
    "--output",
    default=Path("."),
    type=click.Path(dir_okay=True, file_okay=False),
    help="The output directory",
)
def main(output):
    """Download the Oxford Flower Dataset [NilsZiss2008]_ using Torchvision.

    .. [NilsZiss2008] Nilsback, M-E. and Zisserman, A., *Automated flower
       classification over a large number of classes*, Proceedings of the
       Indian Conference on Computer Vision, Graphics and Image Processing
       (2008)
    """
    Flowers102(root=output, download=True)


if __name__ == "__main__":
    main()
