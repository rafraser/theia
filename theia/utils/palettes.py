from theia.utils.color import Color, tidy_color, color_to_hex, distance_squared
from PIL import Image, ImageColor
from sklearn.cluster import KMeans
import os, requests

# Extension to use for palette files
# Palettes are saved as unencoded plain text, one color per line
PALETTE_EXT = "txt"

ColorPalette = dict[str, Color]


def load_palette(name: str) -> ColorPalette:
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
        return parse_palette([line for line in f.readlines()])


def load_or_download_palette(name: str, save: bool = True) -> ColorPalette:
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


def parse_palette(strings: list[str]) -> ColorPalette:
    """Parse a list of strings into a list of colors

    Args:
        strings (list[str]): List of possible color strings

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
            result[line_data[0]] = ImageColor.getrgb(line_data[1])
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


def parse_unnamed_palette(strings: list[str]) -> list[Color]:
    """Parse a list of strings into a list of colors

    Args:
        strings (list[str]): List of possible color strings

    Returns:
        list[Color]: List of parsed RGB colors
    """
    return [ImageColor.getrgb(s) for s in strings]


def convert_palette_to_named(
    colors: list[Color], names: list[str] = None
) -> ColorPalette:
    """Convert a list of colors into a named color palette

    Args:
        colors (list[Color]): List of colors

    Returns:
        ColorPalette: Named color palette
    """
    if not names:
        return {str(n): c for n, c in enumerate(colors)}
    else:
        if len(names) != len(colors):
            raise ValueError("Number of names must match number of colors")
        else:
            return {names[n]: c for n, c in enumerate(colors)}


def save_palette(name: str, colors: ColorPalette):
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
        ColorPalette: Parsed colors from the palette
    """
    r = requests.get(f"https://lospec.com/palette-list/{name}.hex")
    if r.status_code != 200:
        raise ValueError("Could not get palette info from lospec!")

    return parse_unnamed_palette(["#" + c for c in r.text.splitlines()])


def download_and_save_lospec_palette(name: str) -> ColorPalette:
    """Download a palette from lospec and save it to a file
    This also returns the saved palette, for your convienence

    Args:
        name (str): Palette name to fetch

    Returns:
        ColorPalette: Parsed colors from the palette
    """
    colors = download_lospec_palette(name)
    save_unnamed_palette(name, colors)
    return convert_palette_to_named(colors)


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


def palette_from_image(image: Image, n: int) -> ColorPalette:
    """Generate a palette of the most dominant colours in an image

    Args:
        image (Image): Image
        n (int): Number of colors to pull

    Returns:
        ColorPalette: Palette of dominant colors. Keys will be numerical, increasing from 0
    """
    clusters = KMeans(n_clusters=n).fit(image.getdata())
    colors = [tidy_color(color) for color in clusters.cluster_centers_]
    return convert_palette_to_named(colors)
