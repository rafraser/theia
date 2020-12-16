import argparse
from theia.utils.color import Color
from theia.utils.gif import combine_frames
from theia.utils.outline import neon_glow
from PIL import Image, ImageColor


def color_from_hue(hue: int) -> Color:
    return ImageColor.getrgb(f"hsv({str(hue)}, 100%, 100%)")


def make_frame(base: Image, hue: int, background: Image = None) -> Image:
    color = color_from_hue(hue)
    canvas = background.copy()
    canvas.alpha_composite(neon_glow(base, color))
    return canvas.convert("RGB")


def main(args):
    base = Image.open(args.input).convert("RGBA")
    background = Image.open(args.background).convert("RGBA")
    background = background.resize(base.size)

    frames = []
    shift = 360 / args.frames
    for i in range(args.frames):
        hue = args.starthue + (shift * i)
        frames.append(make_frame(base, hue, background))
    combine_frames(frames, args.output, framerate=args.framerate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("background")
    parser.add_argument("output")
    parser.add_argument("--starthue", type=int, default=0)
    parser.add_argument("--frames", type=int, default=60)
    parser.add_argument("--framerate", type=int, default=30)
    args = parser.parse_args()
    main(args)
