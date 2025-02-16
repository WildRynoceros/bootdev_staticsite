from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)
    
    def __repr__(self):
        if self.url is None:
            return f'TextNode(text="{self.text}", text_type={self.text_type})'
        else:
            return f'TextNode(text="{self.text}", text_type={self.text_type}, url="{self.url}")'
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag='i', value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag='code', value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag='img', value='', props={'src': text_node.url, 'alt': text_node.text})
        case _:
            raise ValueError('text_node has an unknown TextType')

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_nodes = []
    def process_node(node, delimiter, text_type):
        # TODO: Refactor to be regex?
        new_nodes = []
        split_text = node.text.split(delimiter)
        for idx, text in enumerate(split_text):
            if len(text) == 0:
                continue
            if idx % 2 == 0:
                new_nodes.append(TextNode(text, node.text_type))
            else:
                new_nodes.append(TextNode(text, text_type))
        return new_nodes
    for node in old_nodes:
        final_nodes.extend(process_node(node, delimiter, text_type))
    return final_nodes

def extract_markdown_images(text):
    matches = re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return matches

def process_node_regex(node, pattern, extract_func, text_type):
    new_nodes = []
    split_text = re.split(pattern, node.text)
    links = extract_func(node.text)
    link_idx = 0
    for idx, text in enumerate(split_text):
        # Handle links at beginning/end
        if (len(text) == 0) and (link_idx < len(links)):
            new_nodes.append(TextNode(links[link_idx][0], text_type, url=links[link_idx][1]))
            link_idx += 1
            continue
        # Handle original text and link if available
        elif len(text) != 0:
            new_nodes.append(TextNode(text, node.text_type))
            if link_idx < len(links):
                new_nodes.append(TextNode(links[link_idx][0], text_type, url=links[link_idx][1]))
                link_idx += 1
    return new_nodes

def split_nodes_image(old_nodes):
    pattern = r"!\[[^\[]*\)"
    final_nodes = []

    for node in old_nodes:
        final_nodes.extend(process_node_regex(node, pattern, extract_markdown_images, TextType.IMAGE))
    return final_nodes

def split_nodes_link(old_nodes):
    pattern = r"(?<!!)\[[^\[]*\)"
    final_nodes = []
        
    for node in old_nodes:
        final_nodes.extend(process_node_regex(node, pattern, extract_markdown_links, TextType.LINK))
    return final_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    
if __name__ == '__main__':
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(text)
    print(nodes)