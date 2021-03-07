from os import listdir, path
from PIL import Image
from pathlib import Path


def images_from_path(filepath: str, input_root: str = "input") -> list[str]:
    """Get a list of image paths from a given location

    Args:
        filepath (str): Filepath to load image(s) from
        input_root (str, optional): Extra directory to check, if path cannot be found. Defaults to "input".

    Returns:
        list[str]: Paths to all images found from the given path
    """
    # If the path doesn't exist, check with the input_root added
    # eg. if cat.png doesn't exist, we'll check input/cat.png
    if not path.exists(filepath):
        path_with_root = path.join(input_root, filepath)
        if path.exists(path_with_root):
            filepath = path_with_root
        else:
            return []

    if path.isfile(filepath):
        return [filepath]
    elif path.isdir(filepath):
        return [
            fp for f in listdir(filepath) if path.isfile(fp := path.join(filepath, f))
        ]

    return []


def load_images_from_path(filepath: str, input_root: str = "input") -> list[Image]:
    """Same as the above function, but opens images up with PIL
    All images will be converted to RGBA mode

    Args:
        filepath (str): Filepath to load image(s) from
        input_root (str, optional): Extra directory to check, if path cannot be found. Defaults to "input".

    Returns:
        list[Image]: All images loaded from the given path
    """
    return [
        Image.open(f).convert("RGBA") for f in images_from_path(filepath, input_root)
    ]


def load_from_path(filepath: str, input_root: str = "input") -> list[tuple[str, Image]]:
    """Returns a list of (filename, Image) tuples for a given path
    Filenames will be returned without path data or extension
    All images will be converted to RGBA mode

    Args:
        filepath (str): Filepath to load image(s) from
        input_root (str, optional): Extra directory to check, if path cannot be found. Defaults to "input".

    Returns:
        list[Image]: All images loaded from the given path
    """
    return [
        (Path(f).stem, Image.open(f).convert("RGBA"))
        for f in images_from_path(filepath, input_root)
    ]


def swap_quadrants(im: Image) -> Image:
    """Swap all four quarants of an image
    eg. top left -> bottom right

    This is useful for working on tiling textures

    Args:
        image (Image): Image to swap

    Returns:
        Image: Image with all four quadrants swapped
    """
    x_mid = im.width // 2
    y_mid = im.height // 2
    quad_top_left = im.crop((0, 0, x_mid, y_mid))
    quad_top_right = im.crop((x_mid, 0, im.width, y_mid))
    quad_bottom_left = im.crop((0, y_mid, x_mid, im.height))
    quad_bottom_right = im.crop((x_mid, y_mid, im.width, im.height))

    im.paste(quad_top_left, (x_mid, y_mid))
    im.paste(quad_top_right, (0, y_mid))
    im.paste(quad_bottom_left, (0, x_mid))
    im.paste(quad_bottom_right, (0, 0))
    return im


def wrapped_alpha_composite(im: Image, paste: Image, coord: tuple[int, int]) -> Image:
    """Alpha composite (paste) an image onto a canvas, wrapping across the edges as required

    Args:
        im (Image): Canvas image to paste onto
        paste (Image): Image to paste onto canvas
        coord (tuple[int, int]): Top-left coordinate for pasting

    Returns:
        Image: Canvas image with wrapped pasted image
    """
    corners = (coord[0], coord[1], coord[0] + paste.width, coord[1] + paste.height)

    # Note that alpha_composite is in-place so we can do some recursive trickery without combining results
    # Check the base case - all of the paste fits inside the image
    if (
        corners[0] >= 0
        and corners[2] <= im.width
        and corners[1] >= 0
        and corners[3] <= im.height
    ):
        im.alpha_composite(paste, coord)
        return

    # Recursively split the remainder
    if corners[0] < 0:
        # We have a bit off to the left
        offset = abs(corners[0])
        if offset > paste.width:
            return

        paste_out = paste.crop((0, 0, offset, paste.height))
        paste_in = paste.crop((offset, 0, paste.width, paste.height))
        wrapped_alpha_composite(im, paste_out, (im.width - offset, coord[1]))
        wrapped_alpha_composite(im, paste_in, (0, coord[1]))
    elif corners[2] > im.width:
        # We have a bit off to the right
        offset = corners[2] - im.width
        if offset > paste.width:
            return

        paste_out = paste.crop((paste.width - offset, 0, paste.width, paste.height))
        paste_in = paste.crop((0, 0, paste.width - offset, paste.height))
        wrapped_alpha_composite(im, paste_out, (0, coord[1]))
        wrapped_alpha_composite(im, paste_in, (corners[0], coord[1]))
    elif corners[1] < 0:
        # We have a bit off the top
        offset = abs(corners[1])
        if offset > paste.height:
            return

        paste_out = paste.crop((0, 0, paste.width, offset))
        paste_in = paste.crop((0, offset, paste.width, paste.height))
        wrapped_alpha_composite(im, paste_out, (coord[0], im.height - offset))
        wrapped_alpha_composite(im, paste_in, (coord[0], 0))
    elif corners[3] > im.height:
        # We have a bit off the bottom
        offset = corners[3] - im.height
        if offset > paste.height:
            return

        paste_out = paste.crop((0, paste.height - offset, paste.width, paste.height))
        paste_in = paste.crop((0, 0, paste.width, paste.height - offset))
        wrapped_alpha_composite(im, paste_out, (coord[0], 0))
        wrapped_alpha_composite(im, paste_in, (coord[0], corners[1]))
