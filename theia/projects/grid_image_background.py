from theia.utils.image import load_images_from_path
from theia.utils.channels import multiply
from theia.utils.image import wrapped_alpha_composite, swap_quadrants
import theia.utils.grid as grid

from PIL import Image, ImageColor
import argparse
import random
import itertools
import os


def build_random_grid(size):
    num = random.choice([2, 3, 3, 3, 4, 4, 4, 5, 5, 6])
    return grid.build(size, num)


def build_random_radial_grid(size):
    num_radial = random.randint(1, 3)
    num_angular = random.randint(4, 8)
    offset = random.randint(0, 360)
    has_center = random.random() > 0.9
    return grid.build_radial(size, num_angular, num_radial, offset, has_center)


def main(args):
    def dot(x, y):
        r = 4
        draw.ellipse((x - r, y - r, x + r, y + r), fill="#a29bfe")

    # Seed generator if applicable
    random.seed(args.seed)

    # Create output directory
    path = f"output/grid_images/"
    if args.output:
        path = args.output
    os.makedirs(path, exist_ok=True)

    # Load all emblems from input directory
    mul_color = ImageColor.getrgb(args.fgcolor)
    emblems = load_images_from_path(args.emblems)
    emblems = [multiply(emblem, mul_color) for emblem in emblems]
    random.shuffle(emblems)
    emblem_generator = itertools.cycle(emblems)

    # Build a bunch of random grids
    for i in range(args.count):
        # Build a random grid
        is_radial = args.radial and random.random() > 0.8
        if is_radial:
            grd = build_random_radial_grid(args.size)
        else:
            # If we're using a square grid, drop last row and column for tiling reasons
            grd = build_random_grid(args.size)
            grd = [row[:-1] for row in grd][:-1]

        # Jitter (if applicable)
        if args.jitter:
            grd = grid.jitter(grd, args.jitter, size=512, clamp=True)

        # Sparsify (if applicable)
        if args.sparsify:
            grd = grid.sparsify(grd, args.sparsify)

        # Build image and paste emblems
        img = Image.new("RGBA", (args.size, args.size), color=args.bgcolor)
        for (xx, yy) in grid.flatten(grd):
            emblem = next(emblem_generator)
            esize = random.choice(args.esize)

            emblem = emblem.resize((esize, esize))
            if args.rotate:
                ang = random.choice([-45, -45, -30, -15, 0, 0, 0, 15, 30, 45, 45])
                # ang = random.randint(-args.rotate, args.rotate)
                emblem = emblem.rotate(ang, Image.NEAREST, expand=True)

            wrapped_alpha_composite(img, emblem, (xx - (esize // 2), yy - (esize // 2)))

        img.save(os.path.join(path, f"grid_{i}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("emblems")
    parser.add_argument("--radial", action="store_true")
    parser.add_argument("--size", type=int, default=512)
    parser.add_argument("--esize", "-e", type=int, nargs="*", default=[48, 64, 80])
    parser.add_argument("--jitter", type=int)
    parser.add_argument("--sparsify", type=float)
    parser.add_argument("--rotate", type=int)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--bgcolor", default="#f1f2f6")
    parser.add_argument("--fgcolor", default="#dfe4ea")
    parser.add_argument("--seed")
    args = parser.parse_args()
    main(args)
