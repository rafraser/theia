from theia.color import tidy_color
from sklearn.cluster import KMeans
from collections import Counter
from PIL import Image, ImageDraw
import argparse


def main(args):
    image = Image.open(args.input).convert("RGB")

    # Find and sort dominant colours
    clusters = KMeans(n_clusters=args.num).fit(image.getdata())
    total = len(clusters.labels_)
    group_counts = Counter(clusters.labels_)

    # Draw cool rectangles
    canvas = Image.new(
        "RGB",
        (image.size[0], image.size[1] + args.height + args.gap),
        color=(255, 255, 255),
    )
    draw = ImageDraw.Draw(canvas)
    xx = 0
    for (group, count) in group_counts.most_common():
        size = round((count / total) * image.size[0])
        color = tidy_color(clusters.cluster_centers_[group])
        draw.rectangle((xx, image.size[1] + args.gap, xx + size, canvas.size[1]), color)
        xx += size

    canvas.paste(image, (0, 0))
    canvas.save(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--num", default=5)
    parser.add_argument("--height", type=int, default=32)
    parser.add_argument("--gap", type=int, default=8)
    args = parser.parse_args()
    main(args)
