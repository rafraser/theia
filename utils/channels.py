from PIL import Image, ImageChops, ImageOps


def invert_with_alpha(im: Image):
    r, g, b, a = im.split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb = ImageOps.invert(rgb)

    r2, g2, b2 = rgb.split()
    return Image.merge("RGBA", (r2, g2, b2, a))


def multiply(image, color):
    full_color_image = Image.new("RGBA", image.size, color)
    return ImageChops.multiply(image, full_color_image)


def multiply_no_alpha(image: Image, color):
    full_color_image = Image.new("RGB", image.size, color)
    return ImageChops.multiply(image, full_color_image)
