import argparse
import math
from typing import Callable
from PIL import Image, ImageDraw
from random import randrange, choice, shuffle

# Typings
Point = tuple[int, int]
Row = list[Point]
Grid = list[Row]


def build(size: int, num: int) -> Grid:
    """Build a basic square grid

    Args:
        size (int): Size (width or height) of the grid
        num (int): Number of points in each row and column

    Returns:
        Grid: Simple grid with equally spaced points
    """
    step = size / (num - 1)

    return [
        [(round(step * xn), round(step * yn)) for xn in range(num)] for yn in range(num)
    ]


def build_radial(
    size: int, num_angular: int, num_radius: int, offset: int = 0, center: bool = True
) -> Grid:
    """Build a radial grid

    Args:
        size (int): Size (width or height) of the grid
        num_angular (int): Number of points in each 'circle'
        num_radius (int): Number of 'circles'
        offset (int, optional): Angular offset, in degrees. Defaults to 0.
        center (bool, optional): Add an extra point at the center of the radial grid?. Defaults to True.

    Returns:
        Grid: Radial grid with equally spaced points
    """
    rad_step = (size // 2) / num_radius
    ang_step = (2 * math.pi) / num_angular
    ang_off = math.radians(offset)

    xx = size // 2
    yy = size // 2

    def rad_to_cart(ang, rad):
        return (xx + round(rad * math.cos(ang)), yy + round(rad * math.sin(ang)))

    grid = [
        [
            rad_to_cart(ang_off + (ang_step * an), rad_step * (rn + 1))
            for an in range(num_angular)
        ]
        for rn in range(num_radius)
    ]

    if center:
        grid.insert(0, [(xx, yy)])
    return grid


def jitter(
    grid: Grid,
    min_variance: int = None,
    max_variance: int = None,
    size: int = None,
    clamp: bool = False,
    variance_list: list[int] = None,
) -> Grid:
    """Randomly jitter all points in a grid
    Jitter will apply to both the x and y axises of the grid

    If a variance list is given, each point will be jittered by a random value from the jitter list
    If one of min_variance or max_variance is specified, points will be jittered from -v to v
    If both min_variance or max_variance is specified, points will be jittered from -max to -min or min to max

    Args:
        grid (Grid): Grid points to jitter
        min_variance (int, optional): Minimum jitter amount. Defaults to None.
        max_variance (int, optional): Maximum jitter amount. Defaults to None.
        size (int, optional): Grid size - useful for clamping. Defaults to None.
        clamp (bool, optional): Whether to stop points leaving the bounds. Defaults to False.
        variance_list (list[int], optional): List of possible jitter amounts. Defaults to None.

    Returns:
        Grid: Transformed grid, with each point 'jittered'
    """
    # If no size is specified, grab the largest point we have
    # if jittering a grid twice this could go badly...
    if size == None:
        size = max(grid[0], key=lambda x: x[0])[0]

    # Argument handling - there's a few cases
    # This jit function is then applied to each point to spice em up
    if variance_list is not None and len(variance_list) > 0:

        def jit(val):
            return val + choice(variance_list)

    elif min_variance is None and max_variance is None:

        def jit(val):
            return val

    elif min_variance is None and max_variance is not None:

        def jit(val):
            return val + choice([-1, 1]) * randrange(0, max_variance)

    elif max_variance is None and min_variance is not None:

        def jit(val):
            return val + choice([-1, 1]) * randrange(0, min_variance)

    elif min_variance >= max_variance:

        def jit(val):
            return val + choice([-1, 1]) * min_variance

    def clampf(x):
        # Clamp a point 0 <= x <= size *only* if the clamp flag is enabled
        if clamp:
            return max(0, min(x, size))
        else:
            return x

    # Jit (and optionally clamp) all points in the grid
    return [[(clampf(jit(xx)), clampf(jit(yy))) for (xx, yy) in row] for row in grid]


def shift_rows(
    grid: Grid, offset: int, mod: int = 2, size: int = None, clamp: bool = False
) -> Grid:
    """Shift Nth rows of a grid by a fixed amount

    Args:
        grid (Grid): Grid to shift rows of
        offset (int): How much to shift each column by
        mod (int, optional): Shift every X rows. Defaults to 2.
        size (int, optional): Size of the grid - used if clamping is enabled. Defaults to None.
        clamp (bool, optional): Whether to remove points outside the bounds. Defaults to False.

    Returns:
        Grid: Transformed grid, with shifted rows
    """
    result_grid = []
    for row_index, row in enumerate(grid):
        if row_index % mod == 0:
            result_grid.append(
                [
                    (x_off, yy)
                    for (xx, yy) in row
                    if (x_off := xx + offset) >= 0 and x_off <= size
                ]
            )
        else:
            result_grid.append(row)
    return result_grid


def shift_columns(
    grid: Grid, offset: int, mod: int = 2, size: int = None, clamp: bool = False
) -> Grid:
    """Shift Nth columns of a grid by a fixed amount

    Args:
        grid (Grid): Grid to shift columns of
        offset (int): How much to shift each column by
        mod (int, optional): Shift every X columns. Defaults to 2.
        size (int, optional): Size of the grid - used if clamping is enabled. Defaults to None.
        clamp (bool, optional): Whether to remove points outside the bounds. Defaults to False.

    Returns:
        Grid: Transformed grid, with shifted columns
    """
    result_grid = []
    for row in grid:
        new_row = []
        for col_index, (xx, yy) in enumerate(row):
            if col_index % mod == 0:
                new_row.append((xx, yy + offset))
            else:
                new_row.append((xx, yy))
        result_grid.append(new_row)
    return result_grid


def triangle(grid: Grid, step: int = 1, symmetric: bool = True) -> Grid:
    """Turn a rectangular grid into a triangular grid

    If symmetric is enabled, an isometric triangle will be made
    If symmetric is not enabled, a right angle triangle will be made

    Args:
        grid (Grid): Grid to adjust
        step (int, optional): How many points to remove from each 'level'. Defaults to 1.
        symmetric (bool, optional): Should points be removed from both sides of the row?. Defaults to True.

    Returns:
        Grid: Transformed grid
    """

    def triangle_row(row, shift):
        if shift >= 1:
            ss = shift * step
            return row[ss:-ss] if symmetric else row[ss:]
        else:
            return row

    return [[p for p in triangle_row(row, idx)] for idx, row in enumerate(grid)]


def sparsify(grid: Grid, percentage: float) -> Grid:
    """Drop a certain percentage of points randomly
    This function keeps exactly the given percentage
    for a faster, approximate method use fast_sparsify

    Args:
        grid (Grid): Grid to drop points from
        percentage (float): Percentage of points to keep

    Returns:
        Grid: Transformed grid
    """
    # Determine which points to keep
    row_size = len(grid[0])
    point_indexes = [
        col_index + (row_index * row_size)
        for row_index, row in enumerate(grid)
        for col_index, _ in enumerate(row)
    ]
    keep = round(len(point_indexes) * percentage)
    shuffle(point_indexes)
    points_to_keep = point_indexes[:keep]

    return [
        [
            p
            for col_index, p in enumerate(row)
            if (col_index + (row_index * row_size)) in points_to_keep
        ]
        for row_index, row in enumerate(grid)
    ]


def fast_sparsify(grid: Grid, percentage: float) -> Grid:
    """Drop an approximate percentage of points randomly
    This function randomly evaluates each point - for an exact percentage, use sparsify

    Args:
        grid (Grid): Grid to drop points from
        percentage (float): Percentage chance of keeping each point

    Returns:
        Grid: Transformed grid
    """
    return [[p for p in row if random.random() < percentage] for row in grid]


def flatten(grid: Grid) -> list[Point]:
    """Flatten a grid into a single list of points

    Args:
        grid (Grid): Grid to flatten

    Returns:
        list[Point]: List of (x, y) coordinates
    """
    return [p for row in grid for p in row]


def transpose(grid: Grid) -> Grid:
    """Transpose (swap rows and columns) a grid

    Args:
        grid (Grid): Grid to tranpose

    Returns:
        Grid: Transposed grid
    """
    swapped_grid = [[(yy, xx) for (xx, yy) in row] for row in grid]
    return list(map(list, zip(*swapped_grid)))


def apply(grid: Grid, func: Callable[[Point], Point]) -> Grid:
    """Apply a pointwise function to all points of a grid

    Args:
        grid (Grid): Grid to apply function to
        func (callable): Pointwise transformation function

    Returns:
        Grid: Transformed grid
    """
    return [[func(p) for p in row] for row in grid]


def visualise(grid: Grid, size: int, padding: int):
    """Helper function to visualise a grid

    Not intended for external use
    """
    img = Image.new("RGB", (size + padding * 2, size + padding * 2), color="#2d3436")
    draw = ImageDraw.Draw(img)

    def dot(x, y):
        r = 4
        draw.ellipse((x - r, y - r, x + r, y + r), fill="#a29bfe")

    for (xx, yy) in flatten(grid):
        dot(xx + padding, yy + padding)

    img.save("output/grid_test.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("size", type=int)
    parser.add_argument("num", type=int)
    args = parser.parse_args()

    grid = build(args.size, args.num)
    visualise(grid, 512, 16)
