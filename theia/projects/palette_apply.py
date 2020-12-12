from theia.utils.palettes import load_or_download_palette
from theia.utils.channels import multiply

from PIL import Image
import argparse, os


def main(args):
    colors = load_or_download_palette(args.palette, save=True)
    path = args.output + "/" + args.palette + "/"
    os.makedirs(path, exist_ok=True)

    for image in args.images:
        im = Image.open(f"{args.input}/{image}.png").convert("RGBA")
        for name, color in colors.items():
            im_colorized = multiply(im, color)
            im_colorized.save(f"{path}{image}_{name}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("palette")
    parser.add_argument("--input", default="input")
    parser.add_argument("--output", default="output")
    parser.add_argument("--images", nargs="+", required=True)
    parser.add_argument("--names", nargs="+")
    args = parser.parse_args()
    main(args)
