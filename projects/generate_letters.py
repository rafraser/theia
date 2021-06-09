from PIL import Image, ImageDraw, ImageFont
import argparse
import os

DEFAULT_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def draw_letter(letter, font, resolution):
    midpoint = (resolution[0] // 2, resolution[1] // 2)
    canvas = Image.new("RGBA", resolution, (255, 255, 255, 0))
    draw = ImageDraw.Draw(canvas)
    draw.text(midpoint, letter, font=font, anchor="mm")
    return canvas


def main(args):
    os.makedirs(args.output, exist_ok=True)
    resolution = (256, 256)
    font = ImageFont.truetype(f"{args.font}.ttf", size=resolution[0])

    for letter in args.characters:
        img = draw_letter(letter, font, resolution)
        img.save(os.path.join(args.output, f"{letter}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--font", default="Futura Bold font")
    parser.add_argument("--characters", default=DEFAULT_LETTERS)
    parser.add_argument("--output", default="output")
    # parser.add_argument("--shadow", action="store_true")
    args = parser.parse_args()
    main(args)
