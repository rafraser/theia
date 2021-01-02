from theia.utils.color import Color, average_color, color_image
from theia.utils.palettes import nearest_in_palette

from PIL import Image
import argparse, math, os


def load_file(input: str, file: str, size: int):
    image = Image.open(input + "/" + file).convert("RGB")
    return image.resize((size, size))


def build_palette_mapping(
    colors: list[Color], palette: dict[str, Color]
) -> dict[Color, Color]:
    return {color: nearest_in_palette(color, palette) for color in colors}


def apply_palette_mapping(image: Image, mapping: dict[Color, Color]) -> Image:
    new = image.copy()
    new.putdata([mapping.get(x) for x in image.getdata()])
    return new


def main(args):
    # os.makedirs(args.output, exist_ok=True)

    # Build a palette up from the images in our palette directory
    palette_images = [
        f
        for f in os.listdir(args.palette)
        if os.path.isfile(args.palette + "/" + f) and f.endswith(".png")
    ]
    pixels = {f: load_file(args.palette, f, args.pixelsize) for f in palette_images}
    palette = {f: average_color(pixels[f]) for f in pixels}
    pixels = {palette[f]: pixels[f] for f in palette}

    # Load image and map to palette
    base = Image.open(args.input).convert("RGB")
    colors = [c[1] for c in base.getcolors(100000)]
    color_mapping = build_palette_mapping(colors, palette)

    # Put it all together
    canvas = Image.new("RGBA", tuple([args.pixelsize * x for x in base.size]))
    w, h = base.size
    locations = [
        (y * args.pixelsize, x * args.pixelsize) for x in range(w) for y in range(h)
    ]
    for k, v in enumerate(base.getdata()):
        pixel = pixels.get(color_mapping.get(v))
        canvas.paste(pixel, locations[k])

    canvas.save(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("palette")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--pixelsize", default=32)
    args = parser.parse_args()
    main(args)
