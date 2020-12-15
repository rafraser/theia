from theia.utils.palettes import load_or_download_palette
from theia.utils.channels import multiply
from theia.utils.outline import neon_glow, apply_outline
from theia.utils.color import Color

from PIL import Image
import argparse, os


def mode_basic(image: Image, color: Color) -> Image:
    return multiply(image, color)


def mode_neon(image: Image, color: Color) -> Image:
    return neon_glow(image, color)


def mode_outline(image: Image, color: Color) -> Image:
    return apply_outline(image, color)


OPTIONS = {
    # stop combining onto one line
    "basic": mode_basic,
    "neon": mode_neon,
    "outline": mode_outline,
}


def main(args):
    colors = load_or_download_palette(args.palette, save=True)

    path = f"output/{args.palette}/"
    if args.output:
        path = args.output
    os.makedirs(path, exist_ok=True)

    images = args.images
    if not args.images:
        images = [
            f.replace(".png", "")
            for f in os.listdir(args.input)
            if os.path.isfile(args.input + "/" + f) and f.endswith(".png")
        ]

    mode_function = OPTIONS.get(args.mode)
    if not mode_function:
        raise ValueError("Invalid mode specified!")

    background = None
    if args.background:
        background = Image.open(f"{args.input}/{args.background}.png").convert("RGBA")

    for image in images:
        im = Image.open(f"{args.input}/{image}.png").convert("RGBA")
        for name, color in colors.items():
            if background:
                canvas = background.copy().resize(im.size)
                canvas.alpha_composite(mode_function(im, color))
                canvas.save(f"{path}{image}_{name}.png")
            else:
                mode_function(im, color).save(f"{path}{image}_{name}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("palette")
    parser.add_argument("--input", default="input")
    parser.add_argument("--output")
    parser.add_argument("--images", nargs="+")
    parser.add_argument("--names", nargs="+")
    parser.add_argument("--mode", default="basic")
    parser.add_argument("--background")
    args = parser.parse_args()
    main(args)
