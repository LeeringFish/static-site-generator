import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_all_none(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props(self):
        props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    
