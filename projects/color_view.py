from theia.utils.palettes import load_or_download_palette
from PIL import Image, ImageDraw
import argparse


def main(args):
    colors = load_or_download_palette(args.palette, save=True)

    # Create canvas
    canvas = Image.new("RGB", (1000, 200), color=(54, 57, 63))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 100, 1000, 200), (66, 69, 74))

    # Draw boxes
    xx = 50
    size = round(900 / len(colors))
    for color in colors:
        draw.rectangle((xx, 50, xx + size, 150), colors[color])
        xx += size

    canvas.save(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("palette")
    parser.add_argument("output")
    args = parser.parse_args()
    main(args)
