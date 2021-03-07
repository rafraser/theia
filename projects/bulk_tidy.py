import argparse, os, math
from theia.utils.channels import invert_with_alpha
from theia.utils.image import load_from_path
from PIL import Image


def main(args):
    os.makedirs(args.output, exist_ok=True)
    images = load_from_path(args.input)

    for (name, img) in images:
        # Invert the image
        if args.invert:
            img = invert_with_alpha(img)

        # Pad the image to the given dimensions
        if args.padded:
            pad = args.padded
            canvas = Image.new("RGBA", (pad, pad), color=(255, 255, 255, 0))
            corner = (
                math.floor((pad - img.size[0]) / 2),
                math.floor((pad - img.size[1]) / 2),
            )
            canvas.paste(img, corner, img)
            img = canvas

        # Save to new location
        # If input = output, this will overwrite
        img.save(os.path.join(args.output, f"{name}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--invert", action="store_true")
    parser.add_argument("--padded", type=int)
    args = parser.parse_args()
    main(args)
