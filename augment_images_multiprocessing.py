# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "click",
#   "Pillow",
#   "torchvision",
#   "tqdm",
# ]
# ///

from concurrent.futures import ProcessPoolExecutor
import os
from pathlib import Path
from time import perf_counter

import click
from PIL import Image
from torchvision.transforms.v2 import RandAugment
from tqdm import tqdm

DEFAULT_AUGMENTER = RandAugment()
DEFAULT_OUTPUT = Path("output")


def augment_image(
    file_path,
    output_dir=DEFAULT_OUTPUT,
    n_augments=10,
    augmenter=DEFAULT_AUGMENTER,
):
    stem = file_path.stem
    file_dir = output_dir / stem
    file_dir.mkdir(exist_ok=True)

    with Image.open(file_path) as image:
        for i in range(n_augments):
            augmented = augmenter(image)
            augmented.save(file_dir / (stem + f"_{i:03d}.jpg"))


@click.command()
@click.argument(
    "input_dir",
    default=Path("flowers-102"),
    type=click.Path(dir_okay=True, file_okay=False, exists=True, path_type=Path),
)
@click.option(
    "--n-workers",
    help="The number of workers to use.",
)
def main(input_dir, n_workers=None):
    print("Available cores:", os.process_cpu_count())

    t = perf_counter()
    DEFAULT_OUTPUT.mkdir(exist_ok=True)
    paths = sorted(Path(input_dir).glob("*.jpg"))

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        for result in tqdm(
            executor.map(augment_image, paths),
            total=len(paths),
        ):
            # if the function returns anything we could do something with the
            # result; but augment_image doesn't return anything so we do nothing
            pass
    print(f"Time taken: {perf_counter() - t:.2f}s\n")


if __name__ == "__main__":
    main()
