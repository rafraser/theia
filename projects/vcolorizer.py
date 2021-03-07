from theia.palettes import load_or_download_palette
from theia.channels import multiply, set_alpha_channel
from theia.color import Color
from theia.sourcetools.vmt_templater import convert_folder_to_vtf, generate_vmt

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
        name_basealpha.png      -- Alpha channel override for the base image

    Args:
        name (str): Base image name
        dir (str, optional): Input directory to look for files. Defaults to "input".

    Returns:
        dict: Dictionary containing the base image, and any additional components
    """
    result = {"base": Image.open(f"{dir}/{name}.png").convert("RGBA")}
    options = ["mask", "envmap", "normal", "overlay", "basealpha"]

    for ext in options:
        if os.path.isfile(f"{dir}/{name}_{ext}.png"):
            result[ext] = Image.open(f"{dir}/{name}_{ext}.png").convert("RGBA")

    return result


def validate_components(components: dict):
    # Check that all image sizes are equally
    size = None
    for img in components.values():
        if size and img.size != size:
            raise ValueError("Image component dimensions must match!")
        else:
            size = img.size


def colorize_base(components: dict, color: Color) -> Image:
    """Colorize the main part of an image

    Args:
        components (dict): Dictionary of vcolorizer "components"
        color (Color): Color to apply to image

    Returns:
        Image: Colorized image
    """
    canvas = components["base"].copy()
    # If we have a mask, colorize only that part
    if components.get("mask"):
        colorized_mask = multiply(components["mask"].copy(), color)
        canvas.alpha_composite(colorized_mask)
    else:
        canvas = multiply(canvas, color)

    # Stamp on any overlays after colorizing
    if components.get("overlay"):
        canvas.alpha_composite(components["overlay"])

    return canvas


def main(args):
    path = args.output + "/" + args.directory
    os.makedirs(path, exist_ok=True)
    colors = load_or_download_palette(args.palette, save=True)

    for image in args.images:
        components = load_image_components(image, dir=args.input)
        validate_components(components)

        for name, color in colors.items():
            # Recolorize the base map
            recolorized = colorize_base(components, color)

            # Apply basealpha if required
            if basealpha := components.get("basealpha"):
                recolorized = set_alpha_channel(recolorized, basealpha)

            recolorized.save(f"{path}/{image}_{name}.png")
            generate_vmt(args.vmt, args.output, args.directory, f"{image}_{name}")

        # Copy additional components - normal maps, etc.
        if normal := components.get("normal"):
            normal.save(f"{path}/{image}_{name}_normal.png")

        if envmap := components.get("envmap"):
            envmap.save(f"{path}/{image}_{name}_envmap.png")

    # Convert the folder to .vtf format
    convert_folder_to_vtf(path, path + "/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("palette")
    parser.add_argument("--vmt", default="basic_lightmapped")
    parser.add_argument("directory")
    parser.add_argument("--input", default="input")
    parser.add_argument("--output", default="output/" + timestamp())
    parser.add_argument("--images", nargs="+", required=True)
    main(parser.parse_args())
