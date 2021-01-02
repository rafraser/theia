from theia.utils.color import Color
from theia.utils.palettes import (
    ColorPalette,
    nearest_in_palette,
    load_or_download_palette,
)

from PIL import Image
import argparse, math, os

MAX_COLORS = 1000000


def build_palette_mapping(
    colors: list[Color], palette: ColorPalette
) -> dict[Color, Color]:
    return {color: nearest_in_palette(color, palette) for color in colors}


def apply_palette_mapping(image: Image, mapping: dict[Color, Color]) -> Image:
    new = image.copy()
    new.putdata([mapping.get(x) for x in image.getdata()])
    return new


def main(args):
    os.makedirs(args.output, exist_ok=True)
    images = [
        f
        for f in os.listdir(args.input)
        if os.path.isfile(args.input + "/" + f) and f.endswith(".png")
    ]
    palette = load_or_download_palette(args.palette, save=True)

    for image in images:
        img = Image.open(args.input + "/" + image).convert("RGBA")
        colors = [c[1] for c in img.getcolors(MAX_COLORS)]
        color_mapping = build_palette_mapping(colors, palette)
        img = apply_palette_mapping(img, color_mapping)
        img.save(args.output + "/" + image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("palette")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    main(args)
