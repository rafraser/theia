import unittest
from theia.palettes import parse_palette, parse_palette_from_json

red_rgb = (231, 76, 60)
blue_rgb = (52, 152, 219)

goal_named = {"red": red_rgb, "blue": blue_rgb}
goal_unnamed = {"0": red_rgb, "1": blue_rgb}


class TestPalettes(unittest.TestCase):
    @staticmethod
    def parse(p):
        return parse_palette(p)

    @staticmethod
    def parse_j(p):
        return parse_palette_from_json(p)

    def test_json_parsing_directly(self):
        json = '{"red": "#e74c3c", "blue": "#3498db"}'
        self.assertEqual(self.parse_j(json), goal_named)

    def test_json_palette(self):
        json = '{"red": "#e74c3c", "blue": "#3498db"}'
        self.assertEqual(self.parse(json), goal_named)

    def test_csv_palette_unnamed(self):
        text = "#e74c3c,#3498db"
        self.assertEqual(self.parse(text), goal_unnamed)

    def test_csv_palette_named(self):
        text = "red=#e74c3c,blue=#3498db"
        self.assertEqual(self.parse(text), goal_named)

    def test_csv_palette_named_two(self):
        text = "red: #e74c3c; blue: #3498db"
        self.assertEqual(self.parse(text), goal_named)

    def test_csv_palette_named_three(self):
        text = "red: #e74c3c; blue: #3498db;"
        self.assertEqual(self.parse(text), goal_named)
