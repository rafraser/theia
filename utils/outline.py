from PIL import Image, ImageFilter, ImageOps, ImageChops
from gif import combine_frames

from channels import invert_with_alpha, multiply_no_alpha
from color import clamp, Color


def apply_outline(im: Image, color: Color, width=8, softness=127) -> Image:
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
    a.save("alpha_original.png")
    a = a.point(lambda x: clamp(x * (256 - softness)))
    a.save("alpha_softened.png")

    # Stick everything back together
    result = Image.merge("RGBA", (r, g, b, a))
    result.alpha_composite(im)
    return result


def neon_glow(im: Image, color: Color, width=4, glowfactor=8):
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
