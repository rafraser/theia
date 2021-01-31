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
        return [f for f in os.listdir(filepath) if path.isfile(path.join(filepath, f))]

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
    return [Image.open(f).convert("RGBA") for f in images_from_path(filepath, input_root)]


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
    return [(Path(f).stem, Image.open(f).convert("RGBA")) for f in images_from_path(filepath, input_root)]
