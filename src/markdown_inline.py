import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    cleaned_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_node = node.text.split(delimiter)
                
            if len(split_node) % 2 != 1:
                raise Exception("missing closing delimiter")
            
            for i in range(len(split_node)):
                if i % 2 == 0:
                    cleaned_nodes.append(TextNode(split_node[i], TextType.TEXT))
                else:
                    cleaned_nodes.append(TextNode(split_node[i], text_type))

        else:
            cleaned_nodes.append(node)
    
    return cleaned_nodes

def split_nodes_image(old_nodes):
    cleaned_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)

            if images is False:
                cleaned_nodes.append(node)
            
            else:
                node_text = node.text
                
                for image in images:
                    split_node = node_text.split(f'![{image[0]}]({image[1]})', 1)
                    cleaned_nodes.append(TextNode(split_node[0], TextType.TEXT))
                    cleaned_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    node_text = split_node[1]
                
                if node_text != "":
                    cleaned_nodes.append(TextNode(node_text, TextType.TEXT))

        else:
            cleaned_nodes.append(node)
    
    return cleaned_nodes

def split_nodes_link(old_nodes):
    cleaned_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)

            if links is False:
                cleaned_nodes.append(node)
            
            else:
                node_text = node.text
                
                for link in links:
                    split_node = node_text.split(f'[{link[0]}]({link[1]})', 1)
                    cleaned_nodes.append(TextNode(split_node[0], TextType.TEXT))
                    cleaned_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    node_text = split_node[1]
                
                if node_text != "":
                    cleaned_nodes.append(TextNode(node_text, TextType.TEXT))

        else:
            cleaned_nodes.append(node)
    
    return cleaned_nodes

def text_to_textnodes(text):
    cleaned_nodes = [TextNode(text, TextType.TEXT)]
    delimiters = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE
    }
    
    for delimiter, text_type in delimiters.items():
        cleaned_nodes = split_nodes_delimiter(cleaned_nodes, delimiter, text_type)
    
    cleaned_nodes = split_nodes_image(cleaned_nodes)
    cleaned_nodes = split_nodes_link(cleaned_nodes)
    return cleaned_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links