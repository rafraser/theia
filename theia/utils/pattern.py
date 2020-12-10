from PIL import Image
from typing import Callable, Union
from utils.color import (
    Color,
    Gradient,
    color_image,
    gradient_image,
    parse_gradient_string,
)

CustomPattern = Callable[[], Image]
Pattern = Union[Color, Gradient]


def generate_image_from_pattern(
    pattern: Union[Pattern, str], size: tuple[int, int]
) -> Image:
    """Generate a image from a pattern type
    This is essentially a case statement - see the component methods for more details

    Args:
        pattern (Pattern): Pattern (or pattern string) to generate image of
        size (tuple[int, int]): Image dimensions

    Raises:
        ValueError: If an invalid pattern is given

    Returns:
        Image: Image with generated pattern
    """
    if callable(pattern):
        return pattern(size)
    elif isinstance(pattern, dict):
        return gradient_image(pattern, size)
    elif isinstance(pattern, tuple):
        return color_image(pattern, size)
    elif isinstance(pattern, str):
        parsed_pattern = parse_pattern_string(pattern)
        return generate_image_from_pattern(parsed_pattern, size)
    else:
        raise ValueError("Unknown pattern type!")


def parsed_pattern(string: str) -> Pattern:
    """Parse some form of pattern string into a valid pattern type

    Not yet fully implemented - this will only attempt to convert to Color or Gradient

    Args:
        string (str): Raw pattern string

    Returns:
        Pattern: Parsed pattern details
    """
    if "," in string:
        return parse_gradient_string(string)
    else:
        return ImageColor.getrgb(string)


def parse_pattern_palette(path: str) -> list[Pattern]:
    """Parse a palette file into a list of patterns

    For info on what color strings can be handled:
    https://pillow.readthedocs.io/en/stable/reference/ImageColor.html

    Returns:
        list[Color]: List of RGB colors
    """
    with open(path) as f:
        return [parsed_pattern(line) for line in f.readlines()]
