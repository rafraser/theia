from theia.utils.color import Color, color_to_hex
from PIL import ImageColor
import os, requests

# Extension to use for palette files
# Palettes are saved as unencoded plain text, one color per line
PALETTE_EXT = "txt"


def load_palette(name: str) -> dict[str, Color]:
    """Parse a palette file into a list of colors
    This loads from the palettes/ directory

    For info on what color strings can be handled:
    https://pillow.readthedocs.io/en/stable/reference/ImageColor.html

    Args:
        name (str): Palette name. Should be a file in the palettes/ directory.

    Returns:
        list[Color]: List of RGB colors
    """
    with open(f"palettes/{name}.{PALETTE_EXT}") as f:
        return parse_palette(
            [line for line in f.readlines() if not line.startswith(";")]
        )


def load_or_download_palette(name: str, save: bool = True) -> dict[str, Color]:
    """Attempts to load a palette from the given palette file
    If the palette does not exist, this will attempt to download the palette from lospec

    Args:
        name (str): Palette name.
        save (bool, optional): If the palette is downloaded, should a copy be saved? Defaults to True.

    Returns:
        list[Color]: List of RGB colors
    """
    try:
        return load_palette(name)
    except FileNotFoundError:
        if save:
            return download_and_save_lospec_palette(name)
        else:
            return download_lospec_palette(name)


def parse_palette(strings: list[str]) -> dict[str, Color]:
    """Parse a list of strings into a list of colors

    Args:
        strings (list[str]): List of possible color strings

    Returns:
        dict[str, Color]: Palette dictionary mapping names to colors
    """
    result = {}
    unnamed = 0
    for s in strings:
        if "=" in s:
            c = s.split("=")
            result[c[0]] = ImageColor.getrgb(c[1])
        else:
            result[str(unnamed)] = ImageColor.getrgb(s)
            unnamed += 1
    return result


def parse_unnamed_palette(strings: list[str]) -> list[Color]:
    """Parse a list of strings into a list of colors

    Args:
        strings (list[str]): List of possible color strings

    Returns:
        list[Color]: List of parsed RGB colors
    """
    return [ImageColor.getrgb(s) for s in strings]


def convert_palette_to_named(colors: list[Color], names: None) -> dict[str, Color]:
    """Convert a list of colors into a named color palette

    Args:
        colors (list[Color]): [description]

    Returns:
        dict[str, Color]: [description]
    """
    if not names:
        return {str(n): c for n, c in enumerate(colors)}
    else:
        if len(names) != len(colors):
            raise ValueError("Number of names must match number of colors")
        else:
            return {names[n]: c for n, c in enumerate(colors)}


def save_palette(name: str, colors: dict[str, Color]):
    """Save a given palette into a text file
    This will save into the palettes/ directory

    Args:
        name (str): Palette name
        colors (list[Color]): List of RGB colors to save
    """
    os.makedirs("palettes", exist_ok=True)
    with open(f"palettes/{name}.{PALETTE_EXT}", "w") as f:
        f.writelines(
            [name + "=" + color_to_hex(c) + "\n" for name, c in colors.items()]
        )


def save_unnamed_palette(name: str, colors: list[Color]):
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
        dict[str, Color]: Parsed colors from the palette
    """
    r = requests.get(f"https://lospec.com/palette-list/{name}.hex")
    if r.status_code != 200:
        raise ValueError("Could not get palette info from lospec!")

    return parse_unnamed_palette(["#" + c for c in r.text.splitlines()])


def download_and_save_lospec_palette(name: str) -> dict[str, Color]:
    """Download a palette from lospec and save it to a file
    This also returns the saved palette, for your convienence

    Args:
        name (str): Palette name to fetch

    Returns:
        dict[str, Color]: Parsed colors from the palette
    """
    colors = download_lospec_palette(name)
    save_unnamed_palette(name, colors)
    return convert_palette_to_named(colors)
