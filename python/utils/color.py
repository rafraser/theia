from typing import Callable
from math import floor
from PIL import Image, ImageColor, ImageDraw

Color = tuple[int, int, int]
Gradient = dict[float, Color]


def parse_palette(path: str) -> list[Color]:
    """Parse a palette file into a list of colors

    For info on what color strings can be handled:
    https://pillow.readthedocs.io/en/stable/reference/ImageColor.html

    Returns:
        list[Color]: List of RGB colors
    """
    with open(path) as f:
        return [ImageColor.getrgb(line) for line in f.readlines()]


def clamp(val: float) -> int:
    """Clamp a number to that expected by a reasonable RGB component
    This ensures that we don't have negative values, or values exceeding one byte
    Additionally, all number inputs are rounded

    Args:
        val (float): Raw float value to clamp

    Returns:
        int: Clamped R/G/B value
    """
    return floor(min(max(0, val), 255))


def linear_interpolate(color1: Color, color2: Color, p: float) -> Color:
    """Linearly interpolate between two colors

    Args:
        color1 (Color): Starting color
        color2 (Color): Ending color
        p (float): position to interpolate. 0 returns first color, 0.5 midpoint, 1 end color

    Returns:
        Color: Interpolated color
    """
    r = color1[0] + (color2[0] - color1[0]) * p
    g = color1[1] + (color2[1] - color1[1]) * p
    b = color1[2] + (color2[2] - color1[2]) * p
    return (floor(r), floor(g), floor(b))


def interpolate(
    color1: Color, color2: Color, p: float, f: Callable[[float], float]
) -> Color:
    """Generic color interpolation function

    Args:
        color1 (Color): Starting color
        color2 (Color): Ending color
        p (float): position to interpolate
        f (Callable[[float], float]): Interpolation function. Should map 0..1 to 0..1

    Returns:
        Color: [description]
    """
    return linear_interpolate(color1, color2, f(p))


def gradient(stops: Gradient, t: float) -> Color:
    """Gradient utility function
    Given some value of t, will return the interpolated value for that gradient

    Args:
        stops (Gradient): List of gradient stops: (float, color)
        t (float): 0..1 position of the gradient

    Returns:
        Color: Interpolated color value
    """
    laststop = None
    for stop in stops:
        if laststop is not None and t <= stop:
            d = (t - laststop) / (stop - laststop)
            c1 = stops[laststop]
            c2 = stops[stop]
            return linear_interpolate(c1, c2, d)
        laststop = stop

    # Return last color if it doesn't fit into a stop
    return list(stops.values())[-1]


def linspace_gradient(clrs: list[Color]) -> Gradient:
    """Given a list of colors, generate a linearly spaced gradient stops
    First element will be at point 0, last element at point 1, etc.

    Args:
        clrs (list[Color]): List of colors

    Returns:
        Gradient: Linearly spaced gradient stops, using the specified colors
    """
    return {i / (len(clrs) - 1): c for i, c in enumerate(clrs)}


def parse_gradient_string(string: str) -> Gradient:
    """Parse a comma-seperated list of colors and generate a basic gradient
    Supports any color string supported by PIL.ImageColor

    Args:
        string (str): Gradient string

    Returns:
        Gradient: Linearly spaced gradient stops
    """
    return linspace_gradient([ImageColor.getrgb(c.strip()) for c in string.split(",")])


def gradient_image(stops: Gradient, size: tuple[int, int]) -> Image:
    """Generate an image from gradient stops
    This image will always run Left to Right
    For different directions, use Image.rotate on the result

    Args:
        stops (dict[float, Color]): Gradient stops
        size (tuple[int, int]): Image dimensions
    Returns:
        Image: Gradient image (RGBA)
    """
    canvas = Image.new("RGBA", size)
    draw = ImageDraw.Draw(canvas)

    for i in range(size[0]):
        t = i / (size[0] - 1)
        color = gradient(stops, t)
        draw.line((i, 0, i, size[1]), fill=color)
    return canvas


def color_image(color: Color, size: tuple[int, int]) -> Image:
    """Generate an image from a single color

    Args:
        color (Color): Base color
        size (tuple[int, int]): Image dimensions

    Returns:
        Image: image made with a single color
    """
    return Image.new("RGBA", size, color=color)
