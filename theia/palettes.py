from theia.color import Color, color_to_hex, distance_squared
from PIL import ImageColor
import json
import os
import re
import requests

# Extension to use for palette files
# Palettes are saved as unencoded plain text, one color per line
PALETTE_EXT = "txt"

ColorPalette = dict[str, Color]


def parse_palette(content: str,
                  allow_download: bool = True,
                  save_downloaded: bool = True,
                  palette_dir: str = "palettes") -> ColorPalette:
    """Attempt to parse a palette from a given string

    This works in the following order:
        - Load locally saved palettes from the given directory
        - Attempt to download from a URL, if applicable
        - Attempt to parse as a JSON object
        - Attempt to read as a CSV palette
        - Attempt to download from the Lospec palette API

    If you know in advance what format this palette string will be in,
    see the rest of this module for specific handler functions

    Args:
        content (str): Palette string to attempt to parse
        allow_download (bool, optional): Whether to attempt to download palettes if a URL is given. Defaults to True.
        save_downloaded (bool, optional): Whether to save any palettes that are downloaded. Defaults to True.
        palette_dir (str, optional): Palette directory to save/load local palettes. Defaults to "palettes".

    Returns:
        ColorPalette: [description]
    """
    # Prioritise local palettes above all else
    try:
        load_palette_file(content, palette_dir=palette_dir)
    except FileNotFoundError:
        pass

    # If this looks like a URL, try downloading the palette
    if allow_download and (content.startswith("http:") or content.startswith("https:")):
        return download_palette_from_url(content, save=save_downloaded, palette_dir=palette_dir)

    # Attempt to parse as a JSON palette
    try:
        return parse_palette_from_json(content)
    except json.JSONDecodeError:
        pass

    # We've exhausted the main options! What we do next depends on commas
    # If we have commas: this is probably a csv palette format
    # If we don't: probably a Lospec palette identifier
    if "," in content:
        return parse_palette_lines(content.split(","))
    else:
        lospec_url = f"https://lospec.com/palette-list/{content}"
        return download_palette_from_url(lospec_url, save=save_downloaded, palette_dir=palette_dir)


def parse_palette_lines(strings: list[str]) -> ColorPalette:
    """Parse a list of strings into a ColorPalette

    Args:
        strings (list[str]): List of possible color strings.
                             These can include names or be standalone colors.

    Returns:
        ColorPalette: Palette dictionary mapping names to colors
    """
    result = {}
    unnamed = 0
    for s in strings:
        # Ignore comments
        if s.startswith(";") or s.startswith("//") or s.startswith("/*"):
            continue

        # Ignore blank lines
        if len(s.strip()) < 1:
            continue

        # Attempt to determine color names seperated by = or :
        line_data = s
        if "=" in s:
            line_data = [clean_symbols(x) for x in s.split("=")]
        elif ":" in s:
            line_data = [clean_symbols(x) for x in s.split(":")]

        if isinstance(line_data, list):
            color_name = tidy_color_name(line_data[0])
            color_value = ImageColor.getrgb(line_data[1])
            result[color_name] = color_value
        else:
            result[str(unnamed)] = ImageColor.getrgb(clean_symbols(line_data))
            unnamed += 1

    return result


def clean_symbols(word: str) -> str:
    """Remove all non alphanumeric characters from a string

    Args:
        word (str): String to cleanse

    Returns:
        str: Cleansed string
    """
    return "".join([c for c in word if c.isalnum() or c == "#"])


def tidy_color_name(word: str) -> str:
    """Tidy up a string to make it suitable for a color name in a palette
    This replaces whitespace with underscores, and lowers the text

    Args:
        word (str): Color name to tidy up

    Returns:
        str: Tidied color name
    """
    return word.replace(" ", "_").lower()


def load_palette_file(name: str, palette_dir: str = "palettes") -> ColorPalette:
    """Parse a palette file into a list of colors
    This loads from the palettes/ directory

    For info on what color strings can be handled:
    https://pillow.readthedocs.io/en/stable/reference/ImageColor.html

    Args:
        name (str): Palette name. Should be a file in the palettes/ directory.

    Returns:
        list[Color]: List of RGB colors
    """
    palette_file = os.path.join(palette_dir, f"{name}.{PALETTE_EXT}")
    with open(palette_file) as f:
        return parse_palette_lines([line for line in f.readlines()])


def save_palette(name: str, colors: ColorPalette, palette_dir: str = "palettes"):
    """Save a given palette into a text file
    This will save into the palettes/ directory

    Args:
        name (str): Palette name
        colors (list[Color]): List of RGB colors to save
        palette_dir (str): Directory to save the file to. Defaults to "palettes"
    """
    os.makedirs(palette_dir, exist_ok=True)
    palette_path = os.path.join(f"{name}.{PALETTE_EXT}")
    with open(palette_path, "w") as f:
        f.writelines(
            [name + "=" + color_to_hex(c) + "\n" for name, c in colors.items()]
        )


def parse_palette_from_json(content: str) -> ColorPalette:
    """Parse a color palette from a JSON string
    The keys will be used as the color names, and the values converted to color values

    Complicated JSON objects will throw an error - ensure that the JSON given is only one level deep

    Args:
        content (str):

    Returns:
        ColorPalette: Parsed color palette
    """
    palette = json.loads(content)
    return {tidy_color_name(k): ImageColor.getrgb(v) for k, v in palette.items()}


def download_palette_from_url(url: str, save: bool = True, palette_dir: str = "palettes") -> ColorPalette:
    """Attempt to load a color palette from the given URL

    Supported palette hosts:
        Lospec

    Args:
        url (str): URL to palette
        save (bool, optional): Whether this palette should be saved once downloaded. Defaults to True.
        palette_dir (str, optional): Where to save downloaded palettes to. Defaults to "palettes".

    Returns
        ColorPalette: ColorPalette obtained from the given URL
    """
    # Lospec palettes
    if m := re.match(r"https:\/\/lospec\.com\/palette-list\/(\S+)"):
        name = m.group(1)
        palette = download_lospec_palette(name)

    if palette:
        if save:
            save_palette(name, palette, palette_dir)
        return palette
    else:
        raise ValueError("URL is not recognised as a support palette host")


def download_lospec_palette(name: str) -> ColorPalette:
    """Download a palette name from lospec
    This does not save the palette - see the below function to save palettes

    Args:
        name (str): Palette name to fetch: see https://lospec.com/palette-list

    Raises:
        ValueError: If palette info could not be obtained from lospec

    Returns:
        ColorPalette: Parsed colors from the palette
    """
    r = requests.get(f"https://lospec.com/palette-list/{name}.hex", timeout=5)
    if r.status_code != 200:
        raise RuntimeError("Could not get palette info from lospec!")
    return parse_palette_lines(["#" + c for c in r.text.splitlines()])


def nearest_in_palette(
    target: Color, palette: ColorPalette, cache: dict[Color, Color] = None
) -> Color:
    """Find a color in a palette closest to a given color

    Args:
        target (Color): Color to match
        palette (ColorPalette): Palette with possible color options
        cache (dict, optional): Optional cache to boost performance

    Returns:
        Color: One color from the given palette
    """
    # cache lookup
    if cache and target in cache:
        return cache.get(target)

    best_color = min(palette.values(), key=lambda c: distance_squared(c, target))
    if cache:
        cache[target] = best_color
    return best_color
