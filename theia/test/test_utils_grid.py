import unittest
import theia.utils.grid as grid

grid_test_base = [
    [(0, 0), (10, 0), (20, 0), (30, 0), (40, 0), (50, 0)],
    [(0, 10), (10, 10), (20, 10), (30, 10), (40, 10), (50, 10)],
    [(0, 20), (10, 20), (20, 20), (30, 20), (40, 20), (50, 20)],
    [(0, 30), (10, 30), (20, 30), (30, 30), (40, 30), (50, 30)],
    [(0, 40), (10, 40), (20, 40), (30, 40), (40, 40), (50, 40)],
    [(0, 50), (10, 50), (20, 50), (30, 50), (40, 50), (50, 50)],
]


class TestGrid(unittest.TestCase):
    def test_build(self):
        self.assertEqual(grid.build(size=50, num=6), grid_test_base)


if __name__ == "__main__":
    unittest.main()
