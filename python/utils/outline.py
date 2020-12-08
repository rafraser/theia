from PIL import Image, ImageFilter, ImageOps, ImageChops
from utils.channels import invert_with_alpha, multiply_no_alpha
from utils.color import clamp, Color


def apply_outline(
    im: Image, color: Color, width: int = 8, softness: int = 127
) -> Image:
    """Apply an outline to an image

    Args:
        im (Image): Image to apply outline to. Must be in RGBA format.
        color (Color): Color of the outline.
        width (int, optional): How wide the outline should be. Defaults to 8.
        softness (int, optional): Softening for the outline - 0 for no softening, 255 for 'glow'. Defaults to 127.

    Returns:
        Image: Image with applied outline
    """
    # The base RGB channels are just whatever we want the outline color to be
    r, g, b = Image.new("RGB", im.size, color).split()

    # Blur our image and apply softness filter
    blurred = im.filter(ImageFilter.GaussianBlur(width))
    _, _, _, a = blurred.split()
    a = a.point(lambda x: clamp(x * (256 - softness)))

    # Stick everything back together
    result = Image.merge("RGBA", (r, g, b, a))
    result.alpha_composite(im)
    return result


def neon_glow(im: Image, color: Color, width: int = 4, glowfactor: int = 8):
    """Apply a 'neon' glow to an image
    This consists of a stronger outline, followed by a very soft outline for the glow

    Args:
        im (Image): Image to apply neon glow to. Must be in RGBA format.
        color (Color): Color for the neon glow
        width (int, optional): Width of the inner outline. Defaults to 4.
        glowfactor (int, optional): Scale of the glow outline, compared to the inner outline. Defaults to 8.

    Returns:
        Image: Image with neon glow applied
    """
    im = apply_outline(im, color, width=width, softness=32)
    im = apply_outline(im, color, width=width * glowfactor, softness=255)
    return im


def drop_shadow(
    im: Image,
    radius: int = 8,
    color: Color = (0, 0, 0),
    strength: float = 0.8,
    offset: tuple[int, int] = (8, 8),
) -> Image:
    """Apply a drop shadow to a given image

    Args:
        im (Image): Base image
        radius (int, optional): Blur radius. Defaults to 8.
        color (Color, optional): Shadow color. Defaults to (0, 0, 0).
        strength (float, optional): Alpha multiplier. Defaults to 0.8.
        offset (tuple[int, int], optional): Shadow offset. Defaults to (8, 8).

    Returns:
        Image: output image, with composited drop shadow
    """
    # Base channels are what we want the shadow color to be
    r, g, b = Image.new("RGB", im.size, color).split()

    # Blur our original image and extract alpha channel
    # Multiply by the shadow strength
    blurred = im.filter(ImageFilter.GaussianBlur(radius))
    _, _, _, a = blurred.split()
    a = a.point(lambda x: clamp(x * strength))

    # Stick things back together to obtain our basic shadow
    result = Image.merge("RGBA", (r, g, b, a))

    # Arrange everything neatly on a canvas
    canvas = Image.new(
        "RGBA", [sum(x) for x in zip(im.size, offset)], (255, 255, 255, 0)
    )
    canvas.paste(result, offset, result)
    canvas = canvas.crop((0, 0, im.size[0], im.size[1]))
    canvas = Image.alpha_composite(canvas, im)
    return canvas


def drop_shadow_simple(im: Image, strength: int = 8) -> Image:
    """Simplified version of the above function

    Args:
        im (Image): Image to apply drop shadow to
        strength (int, optional): Shadow intensity. Defaults to 8.

    Returns:
        Image: Output image, with composited drop shadow
    """
    return drop_shadow(im, radius=strength, offset=(strength, strength))
