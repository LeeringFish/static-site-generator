from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other_node):
        return (self.text == other_node.text
                and self.text_type == other_node.text_type
                and self.url == other_node.url) 
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    type = text_node.text_type
    text = text_node.text
    url = text_node.url
    if type == TextType.TEXT:
        node = LeafNode(None, text)
    elif type == TextType.BOLD:
        node = LeafNode("b", text)
    elif type == TextType.ITALIC:
        node = LeafNode("i", text)
    elif type == TextType.CODE:
        node = LeafNode("code", text)
    elif type == TextType.LINK:
        node = LeafNode("a", text, {"href": url})
    elif type == TextType.IMAGE:
        node = LeafNode("img", "", {"src": url, "alt": text,})
    else:
        raise Exception()
    
    return node


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            if len(parts) < 3:
                raise Exception("invalid markdown syntax")
            new_nodes.extend([TextNode(parts[0], TextType.TEXT),
                              TextNode(parts[1], text_type),
                              TextNode(parts[2], TextType.TEXT),])
        else:
            new_nodes.append(node)
    
    return new_nodes