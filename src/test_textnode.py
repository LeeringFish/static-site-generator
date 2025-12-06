import unittest

from textnode import TextNode, TextType 
from textnode import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("text node", TextType.TEXT)
        node2 = TextNode("text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("text node", TextType.TEXT)
        node2 = TextNode("text node", TextType.TEXT, "http://github.com")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_image_to_html_node(self):
        node = TextNode("Image", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "Image"})

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ])
        
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" word", TextType.TEXT),
                        ])
        
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
                            TextNode("This is text with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word", TextType.TEXT),
                        ])
        
    def test_split_nodes_delimiter_split_twice(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com")], matches)

    def test_multiple_links(self):
        text = "Links: [first](https://a.com) and [second](https://b.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("first", "https://a.com"), ("second", "https://b.com")],
            matches,
    )
        
    def test_multiple_images(self):
        text = "Pics: ![one](https://a.com/1.png) and ![two](https://a.com/2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("one", "https://a.com/1.png"), ("two", "https://a.com/2.png")],
            matches,
    )
        
    def test_link_does_not_match_image(self):
        text = "![img](https://i.com/x.png) and [site](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("site", "https://example.com")],
            matches,
    )
        
    def test_brackets_in_text(self):
        text = "Weird [text [inside]](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("text [inside]", "https://example.com")],
            matches,
    )
        



if __name__ == "__main__":
    unittest.main()

