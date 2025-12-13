import unittest

from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        self.assertEqual("Hello", extract_title(md))
    
    def test_extract_title_again(self):
        md = "# Header One "
        self.assertEqual("Header One", extract_title(md))

    def test_extract_title_no_h1(self):
        md = "## Header Two\n### Header Two"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_no_headers(self):
        md = "Line One\nLine Two"
        with self.assertRaises(ValueError):
            extract_title(md)