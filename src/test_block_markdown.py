import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_line(self):
        md = "Single line of text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Single line of text"])

    def test_markdown_to_blocks_extra_blanks(self):
        md = "First paragraph\n\n\nSecond paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_markdown_to_blocks_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_block_to_block_type_heading(self):
        heading = "# First Heading"
        type = block_to_block_type(heading)
        self.assertEqual(type, BlockType.HEADING)
        another_heading = "### Another Heading"
        another_type = block_to_block_type(another_heading)
        self.assertEqual(another_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md = '```print("Hello, world!")\nx = 1 + 2```'
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = "> This is a quote.\n> It spans multiple lines."
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.QUOTE)

    def test_block_to_block_type_ulist(self):
        md = "- Item one\n- Item two"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_olist(self):
        md = "1. First\n2. Second\n3. Third"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        md = "First line\nSecond line"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)
        