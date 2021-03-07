from theia.color import Color
from theia.palettes import (
    ColorPalette,
    nearest_in_palette,
    load_or_download_palette,
)
from theia.image import load_from_path

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
    images = load_from_path(args.input)
    palette = load_or_download_palette(args.palette, save=True)

    for (name, img) in images:
        colors = [c[1] for c in img.getcolors(MAX_COLORS)]
        color_mapping = build_palette_mapping(colors, palette)
        img = apply_palette_mapping(img, color_mapping)
        img.save(os.path.join(args.output, f"{name}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("palette")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    main(args)
