import unittest
from theia.palettes import parse_palette

palette_test_basic = """
#e74c3c
#3498db
"""

palette_test_basic2 = """
#aaa
"""

palette_test_basic_comments = """
; This is one form of comment
// This is also a comment
#e74c3c
#3498db
"""

palette_test_named = """
red=#e74c3c
blue=#3498db
"""

palette_test_named2 = """
red:#e74c3c
blue:#3498db
"""

palette_test_less = """
/* This is an example of using a LESS format palette */
@red:     #e74c3c;
@blue:    #3498db;
"""

palette_test_sass = """
/* This is an example of using a SASS format palette */
$red:     #e74c3c;
$blue:    #3498db;
"""

red_rgb = (231, 76, 60)
blue_rgb = (52, 152, 219)

goal_named = {"red": red_rgb, "blue": blue_rgb}
goal_unnamed = {"0": red_rgb, "1": blue_rgb}


class TestPalettes(unittest.TestCase):
    @staticmethod
    def parse(p):
        return parse_palette(p.splitlines())

    def test_basic(self):
        self.assertEqual(self.parse(palette_test_basic), goal_unnamed)

    def test_basic2(self):
        self.assertEqual(self.parse(palette_test_basic2), {"0": (170, 170, 170)})

    def test_basic_comments(self):
        self.assertEqual(self.parse(palette_test_basic_comments), goal_unnamed)

    def test_named(self):
        self.assertEqual(self.parse(palette_test_named), goal_named)

    def test_named2(self):
        self.assertEqual(self.parse(palette_test_named2), goal_named)

    def test_less(self):
        self.assertEqual(self.parse(palette_test_less), goal_named)

    def test_sass(self):
        self.assertEqual(self.parse(palette_test_sass), goal_named)


if __name__ == "__main__":
    unittest.main()
