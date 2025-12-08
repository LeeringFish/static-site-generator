import re
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
            split_nodes = []
            if len(parts) % 2 == 0:
                raise Exception("invalid markdown syntax")
            for i in range(len(parts)):
                part = parts[i]
                if part != "":
                    if i % 2 == 0:
                        split_nodes.append(TextNode(part, TextType.TEXT))
                    else:
                        split_nodes.append(TextNode(part, text_type))

            new_nodes.extend(split_nodes)

        else:
            new_nodes.append(node)
    
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            current = node.text
            images = extract_markdown_images(current)
            if len(images) == 0:
                new_nodes.append(node)
                continue

            for image_alt, image_link in images:
                sections = current.split(f"![{image_alt}]({image_link})", 1)
                before = sections[0]
                after = sections[1]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                current = after

            if current:
                new_nodes.append(TextNode(current, TextType.TEXT))    
            
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            current = node.text
            links = extract_markdown_links(current)
            if len(links) == 0:
                new_nodes.append(node)
                continue

            for anchor_text, url in links:
                sections = current.split(f"[{anchor_text}]({url})", 1)
                before = sections[0]
                after = sections[1]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                current = after

            if current:
                new_nodes.append(TextNode(current, TextType.TEXT))    
            
        else:
            new_nodes.append(node)

    return new_nodes


