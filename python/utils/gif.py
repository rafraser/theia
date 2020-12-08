from PIL import Image
import math


def combine_frames(frames: list[Image], output: str, framerate: int = 50) -> None:
    # Chrome has a fun bug where GIFs are limited to 50FPS
    # If we're trying to make a 60FPS GIF, limit this automatically
    #
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
