from theia.utils.palettes import load_or_download_palette
from theia.utils.channels import multiply
from theia.utils.outline import neon_glow, apply_outline
from theia.utils.color import Color
from theia.utils.image import load_from_path

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
    images = load_from_path(args.input)

    path = f"output/{args.palette}/"
    if args.output:
        path = args.output
    os.makedirs(path, exist_ok=True)

    mode_function = OPTIONS.get(args.mode)
    if not mode_function:
        raise ValueError("Invalid mode specified!")

    background = None
    if args.background:
        background = Image.open(args.background).convert("RGBA")

    for (iname, im) in images:
        for cname, color in colors.items():
            if background:
                canvas = background.copy().resize(im.size)
                canvas.alpha_composite(mode_function(im, color))
                canvas.save(os.path.join(path, f"{iname}_{cname}.png"))
            else:
                mode_function(im, color).save(
                    os.path.join(path, f"{iname}_{cname}.png")
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("palette")
    parser.add_argument("--input", default="input")
    parser.add_argument("--output")
    parser.add_argument("--mode", default="basic")
    parser.add_argument("--background")
    args = parser.parse_args()
    main(args)
