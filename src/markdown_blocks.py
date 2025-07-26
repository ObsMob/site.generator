from enum import Enum
import re

from htmlnode import ParentNode
from textnode import TextNode,TextType, text_node_to_html_node
from markdown_inline import text_to_textnodes


class BlockType(Enum): 
    PGRAPH = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    BULLET = "unordered list"
    NUMBER = "ordered list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        cleaned_block = block.strip()
        if cleaned_block != "":
            cleaned_blocks.append(cleaned_block)
    return cleaned_blocks

def block_to_block_type(block):
    lines = block.splitlines()

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEAD

    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    elif all(line.startswith("- ") for line in lines):
        return BlockType.BULLET
    
    elif all(re.match(r"\d+\. ", line) for line in lines):
        return BlockType.NUMBER

    else:
        return BlockType.PGRAPH

def block_to_textnodes(block):
    block_textnodes = []
    is_code = is_code_type(block)

    if is_code is True:
        block_textnodes.append(
            TextNode(block.strip("```"), TextType.CODE)
        )   
    else:    
        lines = block.split("\n")
        
        for line in lines:
            textnode_line = text_to_textnodes(line)
            block_textnodes.extend(textnode_line)
    
    return block_textnodes

def block_textnode_to_htmlnode(textnodes, block):
    html_nodes = []

    if is_list_type(block) is True:
        for node in textnodes:
            node.text = re.sub(r"^(?:\d+\. |- )", "", node.text, count=1)
            list_parent = ParentNode("li", [text_node_to_html_node(node)])
            html_nodes.append(list_parent)
    
    else:
        for node in textnodes:
            
            if is_heading_type(block) is True:
                node.text = re.sub(r"^#{1,6} ", "", node.text, count=1)
            
            if is_quote_type(block) is True:
                if node == textnodes[0]:
                    node.text = re.sub(r"^>", "", node.text, count=1)
                else:
                    node.text = re.sub(r"^>", " ", node.text, count=1)
            
            html_nodes.append(text_node_to_html_node(node))

    return html_nodes
        
def is_list_type(block):
    if (block_to_block_type(block) == BlockType.BULLET or 
        block_to_block_type(block) == BlockType.NUMBER
    ):
        return True
    return False

def is_code_type(block):
    if block_to_block_type(block) == BlockType.CODE:
        return True
    return False

def is_heading_type(block):
    if block_to_block_type(block) == BlockType.HEAD:
        return True
    return False

def is_quote_type(block):
    if block_to_block_type(block) == BlockType.QUOTE:
        return True
    return False

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node = ParentNode("div", [])

    

    for block in blocks:
        block_node = ParentNode("", [])

        block_textnodes = block_to_textnodes(block)
        block_htmlnodes = (
            block_textnode_to_htmlnode(block_textnodes, block)
        )
        
        match block_to_block_type(block):

            case BlockType.HEAD:               
                block_node.tag = f'h{len(block.split(maxsplit=1)[0])}'
            case BlockType.QUOTE:
                block_node.tag = "blockquote"
            case BlockType.BULLET:
                block_node.tag = "ul"
            case BlockType.NUMBER:
                block_node.tag = "ol"
            case BlockType.PGRAPH:
                block_node.tag = "p"
            case BlockType.CODE:
                block_node.tag = "pre" 
            case _:
                raise ValueError("invalid block type")
        
        block_node.children.extend(block_htmlnodes)      
        html_node.children.append(block_node)

    return html_node
    