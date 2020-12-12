from theia.utils.palettes import load_or_download_palette
from theia.utils.channels import multiply
from theia.utils.color import Color

from PIL import Image
from math import floor
import argparse, os, time


def timestamp() -> str:
    """Return a string timestamp, suitable for folder names

    Returns:
        str: Timestamp
    """
    return str(floor(time.time()))


def load_image_components(name: str, dir: str = "input") -> dict:
    """Load a base image and any additional components into a dictionary

    This will look for the following files in the same directory:
        name.png                -- Base image
        name_mask.png           -- Colouring mask
        name_envmap.png         -- Envmapmask / specular mask
        name_normal.png         -- Normal map
        name_overlay.png        -- Anything to be overlaid after the colouring step

    Args:
        name (str): Base image name
        dir (str, optional): Input directory to look for files. Defaults to "input".

    Returns:
        dict: Dictionary containing the base image, and any additional components
    """
    result = {"base": Image.open(f"{dir}/{name}.png").convert("RGBA")}

    for ext in ["mask", "envmap", "normal", "overlay"]:
        if os.path.isfile(f"{dir}/{name}_{ext}.png"):
            result[ext] = Image.open(f"{dir}/{name}_{ext}.png").convert("RGBA")

    return result


def colorize_base(components: dict, color: Color) -> Image:
    """Colorize the main part of an image

    Args:
        components (dict): [description]
        color (Color): [description]

    Returns:
        Image: Colorized image
    """
    canvas = components["base"].copy()
    # If we have a mask, colorize only that part
    if components.get("mask"):
        colorized_mask = multiply(components["mask"].copy(), color)
        canvas = canvas.paste(colorized_mask)
    else:
        canvas = multiply(canvas, color)

    # Stamp on any overlays after colorizing
    if components.get("overlay"):
        canvas = canvas.paste(components["overlay"])

    return canvas


def main(args):
    os.makedirs(args.output, exist_ok=True)
    colors = load_or_download_palette(args.palette, save=True)

    for image in args.images:
        components = load_image_components(image, dir=args.input)

        for name, color in colors.items():
            recolorized = colorize_base(components, color)
            recolorized.save(f"{args.output}/{image}_{name}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("palette")
    parser.add_argument("--input", default="input")
    parser.add_argument("--output", default="output/" + timestamp())
    parser.add_argument("--images", nargs="+", required=True)
    main(parser.parse_args())