import argparse
from PIL import Image, ImageDraw
from random import randrange

# Typings
Point = tuple[int, int]
Row = list[Point]
Grid = list[Row]


def build(size: int, num: int) -> Grid:
    step = size / (num - 1)

    return [
        [(round(step * xn), round(step * yn)) for xn in range(num)] for yn in range(num)
    ]


def build_radial(
    size: int, num_angular: int, num_radius: int, offset: int = 0, center: bool = True
) -> Grid:
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


    # If no size is specified, grab the largest point we have
    # if jittering a grid twice this could go badly...
    if size == None:
        size = max(grid[0], key=lambda x: x[0])[0]

    def jit(val):
        return val + randrange(-variance, variance)

    # I'd love to make this into a neater list comprehension but this will have to suffice
    # - Apply a random jitter to each point
    # - If applicable, filter out any points that go out of bounds
    result_grid = []
    for row in grid:
        result_row = []
        for (xx, yy) in row:
            (jit_x, jit_y) = (jit(xx), jit(yy))
            if clamp:
                if jit_x < 0 or jit_x > size or jit_y < 0 or jit_y > size:
                    continue

            result_row.append((jit_x, jit_y))
        result_grid.append(result_row)
    return result_grid


def shift_rows(
    grid: Grid, offset: int, mod: int = 2, size: int = None, clamp: bool = False
) -> Grid:
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


def flatten(grid: Grid) -> list[Point]:
    return [p for row in grid for p in row]


def visualise(grid: Grid, size: int, padding: int):
    img = Image.new("RGB", (size + padding * 2, size + padding * 2), color="#2d3436")
    draw = ImageDraw.Draw(img)

    def dot(x, y):
        r = 4
        draw.ellipse((x - r, y - r, x + r, y + r), fill="#a29bfe")

    for (xx, yy) in flatten(grid):
        dot(xx + padding, yy + padding)

    img.save("output/grid_test.png")
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("size", type=int)
    parser.add_argument("num", type=int)
    args = parser.parse_args()

    grid = build(args.size, args.num)
    print(grid)
    grid = shift_rows(grid, 32, size=args.size, clamp=True)
    grid = shift_columns(grid, -32, mod=3, size=args.size, clamp=True)
    # grid = jitter(grid, 8, clamp=True)
    print(grid)

    visualise(grid, 512, 16)
    print(grid)
