import argparse, os, requests, re


def download_icons_from_page(url: str, path: str, max_images: int = 0):
    """Download all Flaticons from a given Flaticon search URL

    Args:
        url (str): URL to fetch icons from
        path (str): Output directory
        max_images (int, optional): Maximum number of images to download. If not specified, will continue until fully downloaded.

    Raises:
        Exception: If the URL could not be loaded
    """
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("Could not load page!")

    # Download all IDs we can find on this page
    n = 0
    for x in re.finditer(r"data-id=\"(\d+)\">", resp.text):
        if max_images and n >= max_images:
            return
        download_image(x.group(1), path)
        n += 1

    # If we still have more images to get, check for more pages
    if not max_images or n < max_images:
        if has_next_page(resp.text):
            new_max_images = max(max_images - n, 0)
            new_url = get_next_page_url(url)
            download_icons_from_page(new_url, max_images=new_max_images, path=path)


def has_next_page(content: str) -> bool:
    """Check whether a Flaticon search page has another page

    Args:
        content (str): Contents of the current Flaticon search page

    Returns:
        bool: Whether a next page exists
    """
    return "<span>Next page</span>" in content


def get_next_page_url(url: str) -> str:
    """Get the next page of a Flaticon search

    Args:
        url (str): URL for the current flaticon page

    Returns:
        str: URL for the next flaticon page
    """
    if "/search" in url:
        (base_url, args) = url.split("?", 1)
        split_url = base_url.split("/")
        last_part = base_url.split("/")[-1]
        if last_part.isnumeric():
            split_url[-1] = str(int(last_part) + 1)
            base_url = "/".join(split_url)
        else:
            base_url = base_url + "/2"

        return base_url + "?" + args
    else:
        split_url = url.split("/")
        last_part = url.split("/")[-1]
        if last_part.isnumeric():
            split_url[-1] = str(int(last_part) + 1)
            return "/".join(split_url)
        else:
            return url + "/2"


def download_image(id: str, path: str):
    """Download the png image version for a given Flaticon ID

    Args:
        id (str): Flaticon ID
        path (str): Path to save to
    """
    url = url_from_icon_id(id)
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(f"{path}{id}.png", "wb") as f:
            f.write(resp.content)


def url_from_icon_id(id: str) -> str:
    """Get a downloadable URL from a string ID

    Args:
        id (str): Flaticon ID

    Returns:
        str: URL pointing to the .png file for this icon
    """
    return f"https://image.flaticon.com/icons/png/512/{id[:-3]}/{id}.png"


def main(args):
    os.makedirs(args.path, exist_ok=True)
    download_icons_from_page(args.url, args.path, max_images=args.max)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--path", default="output/saved_images/")
    parser.add_argument("--max", default=0, type=int)
    args = parser.parse_args()
    main(args)
