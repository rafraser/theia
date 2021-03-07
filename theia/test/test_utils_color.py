import unittest

from theia.color import linear_interpolate, interpolate


class TestInterpolation(unittest.TestCase):
    def setUp(self):
        self.color1 = (255, 0, 255)
        self.color2 = (0, 255, 0)

    def test_interpolation_zero(self):
        # Test linear interpolation works at the left endpoint
        self.assertEqual(linear_interpolate(self.color1, self.color2, 0), self.color1)

    def test_interpolation_one(self):
        # Test linear interpolation works at the right endpoint
        self.assertEqual(linear_interpolate(self.color1, self.color2, 1), self.color2)

    def test_interpolation_midpoint(self):
        # Test linear interpolation works at the midpoint
        expected = (127, 127, 127)
        self.assertEqual(linear_interpolate(self.color1, self.color2, 0.5), expected)

    def test_interpolation_advanced1(self):
        # Test interpolation with a quadratic easeout
        f = lambda x: x * (2 - x)
        expected = (63, 191, 63)
        self.assertEqual(interpolate(self.color1, self.color2, 0.5, f), expected)

    def test_interpolation_advanced2(self):
        # Test interpolation with cubic interpolation
        f = lambda x: x ** 3
        expected = (223, 31, 223)
        self.assertEqual(interpolate(self.color1, self.color2, 0.5, f), expected)


if __name__ == "__main__":
    unittest.main()
