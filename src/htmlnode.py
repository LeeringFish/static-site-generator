from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from inline_markdown import strip_delimiters, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        formatted_html = ""
        for k, v in self.props.items():
            formatted_html += f' {k}="{v}"'
        return formatted_html

    def __repr__(self):
        return f"{self.tag} {self.value} {self.children} {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        
        if self.tag is None:
            return self.value
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("parent node must have a tag")
        
        if self.children is None:
            raise ValueError("parent node must have children")
        
        children_string = ""

        for child in self.children:
            children_string += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>'
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.CODE:
            text = strip_delimiters(block, "```")
            code_node = text_node_to_html_node(TextNode(text, TextType.CODE))
            pre_node = HTMLNode(tag="pre", children=[code_node])
            block_nodes.append(pre_node)
        else:
            if type == BlockType.PARAGRAPH:
                children = text_to_children(block)
                block_nodes.append(HTMLNode(tag="p", children=children))
            elif type == BlockType.HEADING:
                level = get_heading_level(block)
                tag = "h" + str(level)
                text = block[level:].lstrip()
                children = text_to_children(text)
                block_nodes.append(HTMLNode(tag=tag, children=children))
            elif type == BlockType.QUOTE:
                children = text_to_children(clean_quote_block(block))
                block_nodes.append(HTMLNode(tag="blockquote", children=children))

    
    return HTMLNode(tag="div", children=block_nodes)


def get_heading_level(text):
    count = 0

    for ch in text:
        if ch == "#":
            count += 1
        else:
            break

    return count

def clean_quote_block(block):
    lines = block.split("\n")
    cleaned = []
    for line in lines:
        line = line.lstrip(">")
        line = line.lstrip()
        cleaned.append(line)

    return "\n".join(cleaned)


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]
