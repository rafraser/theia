from PIL import Image
import math


def combine_frames(frames: list[Image], output: str, framerate: int = 50) -> None:
    """Combine a list of frame images into a single .gif

    Note that Chrome has a fun bug where GIFs are limited to 50FPS
    This function will automatically clamp framerates to 50FPS

    Args:
        frames (list[Image]): List of frame images
        output (str): Path to save output GIF, including extension
        framerate (int, optional): Framerate of the gif. Max of 50FPS. Defaults to 50.
    """
    if framerate == 60:
        framerate = 50
    durations = [math.floor(1000 / framerate)] * len(frames)

    frames[0].save(
        output,
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=durations,
        loop=0,
        transparency=0,
    )
