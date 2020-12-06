from typing import Callable
from math import floor

Color = tuple[int, int, int]


def clamp(val: float) -> float:
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


def gradient(stops: dict[float, Color], t: float) -> Color:
    """Gradient utility function
    Given some value of t, will return the interpolated value for that gradient

    Args:
        stops (dict[float, Color]): List of gradient stops: (float, color)
        t (float): 0..1 position of the gradient

    Returns:
        Color: Interpolated color value
    """
    for i in range(len(stops)):
        if t <= gradient[i][0]:
            # Interpolate between stops i - 1 and stop i
            d = (t - gradient[i - 1][0]) / (gradient[i][0] - stops[i - 1][0])
            c1 = gradient[i - 1][1]
            c2 = gradient[i][1]

            return linear_interpolate(c1, c2, d)

    # Return last color if it doesn't fit into a stop
    return stops[-1][1]
