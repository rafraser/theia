from utils.color import Color
from PIL import Image, ImageChops, ImageOps


def invert_with_alpha(im: Image) -> Image:
    """Invert the RGB values of an image while keeping alpha intact

    Args:
        im (Image): Image to invert

    Returns:
        Image: Inverted image
    """
    r, g, b, a = im.split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb = ImageOps.invert(rgb)

    r2, g2, b2 = rgb.split()
    return Image.merge("RGBA", (r2, g2, b2, a))


def multiply(image: Image, color: Color) -> Image:
    """Multiply an image by a given color
    Only works with RGBA images - see the below function for RGB

    Args:
        image (Image): Base image
        color (Color): Color to multiply by

    Returns:
        Image: Base image multiplied by the color
    """
    full_color_image = Image.new("RGBA", image.size, color)
    return ImageChops.multiply(image, full_color_image)


def multiply_no_alpha(image: Image, color: Color) -> Image:
    """Multiply an image by a given color
    Only works with RGB images - see the above function for RGBA

    Args:
        image (Image): Base image
        color (Color): Color to multiply by

    Returns:
        Image: Base image multiplied by the color
    """
    full_color_image = Image.new("RGB", image.size, color)
    return ImageChops.multiply(image, full_color_image)
