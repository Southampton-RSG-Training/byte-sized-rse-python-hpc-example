# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "click",
#   "Pillow",
#   "torchvision",
# ]
# ///

import sys
from pathlib import Path

import click
from PIL import Image
from torchvision.transforms.v2 import RandAugment

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
    from concurrent.futures import ProcessPoolExecutor
    import os
    from time import perf_counter

    print("Available cores:", os.process_cpu_count())

    t = perf_counter()
    DEFAULT_OUTPUT.mkdir(exist_ok=True)
    all_paths = sorted(Path(input_dir).glob("*.jpg"))

    rank = int(os.environ["SLURM_PROCID"])
    n_tasks = int(os.environ["SLURM_NTASKS"])

    paths = all_paths[rank::n_tasks]

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        for result in executor.map(augment_image, paths):
            # if the function returns anything we could do something with the
            # result; but augment_image doesn't return anything so we do nothing
            pass
    sys.stderr.write(f"Time taken: {perf_counter() - t:.2f}s\n")


if __name__ == "__main__":
    main()
