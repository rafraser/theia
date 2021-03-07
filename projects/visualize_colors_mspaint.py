from theia.color import tidy_color
from sklearn.cluster import KMeans
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import argparse, math

GRAY_255 = (255, 255, 255)
GRAY_222 = (222, 222, 222)
GRAY_192 = (192, 192, 192)
GRAY_128 = (128, 128, 128)
GRAY_0 = (0, 0, 0)


def draw_color_box(
    draw, pos, c_fill, size, c_outer=GRAY_192, c_top=GRAY_128, c_inner=GRAY_0
):
    x0, y0 = pos[0], pos[1]
    x1, y1 = x0 + size + 2, y0 + size + 2

    draw.rectangle((x0, y0, x1, y1), fill=c_outer)
    draw.rectangle((x0 + 1, y0 + 1, x1 - 1, y1 - 1), fill=c_fill)
    draw.line((x0, y1, x0, y0, x1, y0), fill=c_top)
    draw.line((x0 + 1, y1 - 1, x0 + 1, y0 + 1, x1 - 1, y0 + 1), fill=c_inner)


def main(args):
    image = Image.open(args.input).convert("RGB")
    image_for_clusters = image.resize((100, 100))

    # Resize particularly large images
    if any(x >= 300 for x in image.size):
        print("Shrinking..")
        ratio = image.size[1] / image.size[0]
        image = image.resize((300, math.floor(300 * ratio)))

    # Find and sort dominant colours
    clusters = KMeans(n_clusters=args.num).fit(image_for_clusters.getdata())
    total = len(clusters.labels_)
    group_counts = Counter(clusters.labels_)
    color_groups = group_counts.most_common()

    def get_color(idx):
        return tidy_color(clusters.cluster_centers_[color_groups[idx][0]])

    # Draw an MS-Paint style background
    width = image.size[0] + 60
    height = image.size[1] + 96
    canvas = Image.new("RGB", (width, height), color=GRAY_192)
    draw = ImageDraw.Draw(canvas)

    # Load font
    # If you're not running this on Windows, I'm sorry
    font = ImageFont.truetype("segoeui.ttf", size=12)

    # Dropdown menu
    headers = ["File", "Edit", "View", "Image", "Colors", "Help"]
    xx = 4
    for option in headers:
        draw.text((xx, 2), option, font=font, fill=GRAY_0)
        first_w, first_h = draw.textsize(option[0], font=font)
        draw.line((xx + 1, first_h + 4, xx + first_w, first_h + 4), fill=GRAY_0)
        xx += draw.textsize(option, font=font)[0] + 6

    # Tools

    # Palette background
    row_size = math.ceil(args.num / 2)
    palette_size = 35 + row_size * 18
    draw.rectangle((4, height - 66, 4 + palette_size, height - 31), fill=GRAY_255)

    # Selected colors
    draw_color_box(draw, (4, height - 66), GRAY_222, 32)
    draw_color_box(
        draw,
        (4 + 14, height - 66 + 14),
        get_color(1),
        14,
        c_outer=GRAY_128,
        c_top=GRAY_255,
        c_inner=GRAY_192,
    )
    draw_color_box(
        draw,
        (4 + 5, height - 66 + 5),
        get_color(0),
        14,
        c_outer=GRAY_128,
        c_top=GRAY_255,
        c_inner=GRAY_192,
    )

    # Palette colors
    for i in range(len(color_groups)):
        color = get_color(i)
        xx = 40 + (i % row_size) * 18
        yy = height - 66 + (i // row_size) * 18
        draw_color_box(draw, (xx, yy), color, 14)

    # Help text
    draw.line((0, height - 24, width, height - 24), fill=GRAY_128, width=1)
    draw.line((0, height - 26, width, height - 26), fill=GRAY_128, width=1)
    draw.text((2, height - 20), args.helptext, fill=GRAY_0, font=font)

    # Darker "central" background
    draw.rectangle((56, 22, width, height - 71), fill=GRAY_128)

    # Finally, paste the image
    canvas.paste(image, (58, 24))
    canvas.save(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--num", default=12)
    parser.add_argument(
        "--helptext", default="For Help, click Help Topics on the Help Menu"
    )
    args = parser.parse_args()
    main(args)
