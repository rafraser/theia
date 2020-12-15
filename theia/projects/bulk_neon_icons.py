import argparse, os, math
from theia.utils.channels import invert_with_alpha
from theia.utils.flaticon import main as download_flaticons
from theia.projects.bulk_tidy import main as tidy_icons
from theia.projects.palette_apply import main as apply_palette
from PIL import Image


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def main(args):
    working_path = f"input/flaticon_{args.search}/"
    # Download icons from FlatIcon
    print("Downloading icons...")
    flaticon_url = f"https://www.flaticon.com/search?word={args.search}&search-type=icons&license=selection&order_by=4&color=1&stroke=2&grid=small"
    downloader_args = {
        "url": flaticon_url,
        "path": working_path,
        "max": args.max,
    }
    download_flaticons(dotdict(downloader_args))

    print("Tidying up...")
    tidy_args = {
        "input": working_path,
        "output": working_path,
        "invert": True,
        "padded": 768,
    }
    tidy_icons(dotdict(tidy_args))

    print("Applying neon sparkle...")
    neon_args = {
        "palette": args.palette,
        "input": working_path,
        "output": f"output/{args.search}_{args.palette}/",
        "mode": "neon",
    }
    apply_palette(dotdict(neon_args))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("search")
    parser.add_argument("palette")
    parser.add_argument("--max", type=int, default=25)
    args = parser.parse_args()
    main(args)