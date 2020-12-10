from utils.color import Color, color_to_hex
from PIL import ImageColor
import os, requests

# Extension to use for palette files
# Palettes are saved as unencoded plain text, one color per line
PALETTE_EXTENSION = "txt"


def parse_palette(name: str) -> list[Color]:
    """Parse a palette file into a list of colors
    This loads from the palettes/ directory

    For info on what color strings can be handled:
    https://pillow.readthedocs.io/en/stable/reference/ImageColor.html

    Returns:
        list[Color]: List of RGB colors
    """
    with open(f"palettes/{name}.{PALETTE_EXT}") as f:
        return [
            ImageColor.getrgb(line)
            for line in f.readlines()
            if not line.startswith("#")
        ]


def save_palette(name: str, colors: list[Color]):
    """Save a given palette into a text file
    This will save into the palettes/ directory

    Args:
        name (str): Palette name
        colors (list[Color]): List of RGB colors to save
    """
    os.makedirs("palettes", exist_ok=True)
    with open(f"palettes/{name}.{PALETTE_EXT}", "w") as f:
        f.writelines([color_to_hex(c) + "\n" for c in colors])


def download_lospec_palette(name: str) -> list[Color]:
    """Download a palette name from lospec
    This does not save the palette - see the below function to save palettes

    Args:
        name (str): Palette name to fetch: see https://lospec.com/palette-list

    Raises:
        ValueError: If palette info could not be obtained from lospec

    Returns:
        list[Color]: Parsed colors from the palette
    """
    r = requests.get(f"https://lospec.com/palette-list/{name}.hex")
    if r.status_code != 200:
        raise ValueError("Could not get palette info from lospec!")

    return [ImageColor.getrgb("#" + c) for c in r.text.splitlines()]


def download_and_save_lospec_palette(name: str) -> list[Color]:
    """Download a palette from lospec and save it to a file
    This also returns the saved palette, for your convienence

    Args:
        name (str): Palette name to fetch

    Returns:
        list[Color]: Parsed colors from the palette
    """
    colors = download_lospec_palette(name)
    save_palette(name, colors)
    return colors
