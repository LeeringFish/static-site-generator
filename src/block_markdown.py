from enum import Enum

from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

def block_to_block_type(markdown):
    if markdown.startswith("#"):
        type = BlockType.HEADING
    elif markdown.startswith("```") and markdown.endswith("```"):
        type = BlockType.CODE
    elif markdown.startswith(">"):
        type = BlockType.QUOTE
    elif markdown.startswith("- "):
        type = BlockType.UNORDERED_LIST
    elif markdown[0].isdigit():
        type = BlockType.ORDERED_LIST
    else:
        type = BlockType.PARAGRAPH

    return type


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        lines = block.split("\n")
        if all(line.startswith("#") for line in lines if line.strip()):
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                children.append(heading_to_html_node(line))
            continue

        type = block_to_block_type(block)
        if type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif type == BlockType.ORDERED_LIST:
            children.append(olist_to_html_node(block))
        elif type == BlockType.UNORDERED_LIST:
            children.append(ulist_to_html_node(block))

    return ParentNode(tag="div", children=children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    count = 0

    for ch in block:
        if ch == "#":
            count += 1
        else:
            break

    text = block[count + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{count}", children)

def code_to_html_node(block):
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [child])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned = []
    for line in lines:
        cleaned.append(line.lstrip(">").strip())
    text = " ".join(cleaned)
    children = text_to_children(text)

    return ParentNode("blockquote", children)

def olist_to_html_node(block):
    items = block.split("\n")
    children = []
    for item in items:
        text = item[3:]
        inner_children = text_to_children(text)
        children.append(ParentNode("li", inner_children))
    return ParentNode("ol", children)

def ulist_to_html_node(block):
    items = block.split("\n")
    children = []
    for item in items:
        text = item[2:]
        inner_children = text_to_children(text)
        children.append(ParentNode("li", inner_children))
    return ParentNode("ul", children)


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]
