from theia.palettes import load_or_download_palette
from theia.image import load_from_path
from theia.outline import drop_shadow_simple

from PIL import Image
import argparse, math, os

THUMBNAIL_WIDTH = 800
THUMBNAIL_HEIGHT = 450


def center_image_in_frame(image, shadow):
    if image.width > THUMBNAIL_WIDTH or image.height > THUMBNAIL_HEIGHT:
        return None

    foreground = Image.new(
        "RGBA", (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), (255, 255, 255, 0)
    )
    xx = math.floor((THUMBNAIL_WIDTH - image.width) / 2)
    yy = math.floor((THUMBNAIL_HEIGHT - image.height) / 2)
    foreground.paste(image, (xx, yy))

    if shadow:
        foreground = drop_shadow_simple(foreground, strength=2)
    return foreground


def main(args):
    # Load what we need
    colors = load_or_download_palette(args.palette, save=True)
    images = load_from_path(args.input)
    image_frames = [
        (name, center_image_in_frame(image, args.shadow)) for (name, image) in images
    ]

    # Handle output directory
    path = f"output/thumbnails/{args.palette}/"
    if args.output:
        path = args.output
    os.makedirs(path, exist_ok=True)

    # Process all combinations
    for cname, color in colors.items():
        background = Image.new("RGBA", (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), color)
        for (iname, image) in image_frames:
            if not image:
                continue

            # Center in canvas
            canvas = background.copy()
            canvas.alpha_composite(image)
            canvas.save(os.path.join(path, f"{iname}_{cname}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("palette")
    parser.add_argument("--input", default="input/blog_icons")
    parser.add_argument("--output")
    parser.add_argument("--shadow", action="store_true")
    args = parser.parse_args()
    main(args)
