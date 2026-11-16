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
from tempfile import TemporaryDirectory

import click
from torchvision.datasets import Flowers102
from tqdm import tqdm


@click.command()
@click.option(
    "--output",
    default=Path("flowers-102"),
    type=click.Path(dir_okay=True, file_okay=False, path_type=Path),
    help="The output directory",
)
@click.option(
    "--split",
    default="train",
    type=click.Choice(["train", "test", "val", "all"]),
    help="The output directory",
)
def main(output, split):
    """Download the Oxford Flower Dataset [NilsZiss2008]_ using Torchvision.

    .. [NilsZiss2008] Nilsback, M-E. and Zisserman, A., *Automated flower
       classification over a large number of classes*, Proceedings of the
       Indian Conference on Computer Vision, Graphics and Image Processing
       (2008)
    """
    output.mkdir(parents=True, exist_ok=True)
    if get_all := (split == "all"):
        split = "test"
    with TemporaryDirectory() as temp_dir:
        click.echo("Downloading data:")
        dataset = Flowers102(root=temp_dir, split=split, download=True)
        # extract the training images into the output directory
        click.echo("Copying files:")
        if get_all:
            files = list(dataset._images_folder.iterdir())
        else:
            files = dataset._image_files
        for path in tqdm(files):
            path.copy_into(output)


if __name__ == "__main__":
    main()
