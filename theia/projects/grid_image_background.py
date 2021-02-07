from theia.utils.image import load_images_from_path
from theia.utils.channels import multiply
from theia.utils.image import wrapped_alpha_composite, swap_quadrants
import theia.utils.grid as grid

from PIL import Image, ImageDraw, ImageColor
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
        # If we're using a square grid, drop last row and column for tiling reasons
        is_radial = random.random() > 0.8
        if is_radial:
            grd = build_random_radial_grid(args.size)
        else:
            grd = build_random_grid(args.size)
            grd = [row[:-1] for row in grd][:-1]

        size_padded = args.size + (args.padding * 2)
        img = Image.new("RGBA", (size_padded, size_padded), color=args.bgcolor)
        draw = ImageDraw.Draw(img)

        for (xx, yy) in grid.flatten(grd):
            emblem = next(emblem_generator)
            esize = random.randint(80, 96)

            x = xx + args.padding
            y = yy + args.padding

            emblem = emblem.resize((esize, esize))
            wrapped_alpha_composite(img, emblem, (x - (esize // 2), y - (esize // 2)))

        img.save(os.path.join(path, f"grid_{i}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("emblems")
    parser.add_argument("--size", type=int, default=480)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--padding", type=int, default=0)
    parser.add_argument("--bgcolor", default="#dfe4ea")
    parser.add_argument("--fgcolor", default="#ffffff")
    parser.add_argument("--seed")
    args = parser.parse_args()
    main(args)
