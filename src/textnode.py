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
        # TODO: Refactor to be regex? And handle other text_types if they exist already
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
    # TODO: Be a bit more proactive if text_type isn't text
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
            new_nodes.append(TextNode(text, node.text_type, node.url))
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

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    if not isinstance(blocks, list):
        blocks = [markdown]
    blocks = [block.strip() for block in blocks]
    return blocks

def block_to_block_type(block):
    # Headings
    if block[0] == '#':
        try:
            if block[0:block.index(' ') + 1] in [('#' * i) + ' ' for i in range(1, 7)]:
                return 'HEADING'
        except ValueError:
            pass
    # Code
    if block[0:3] == '```' and block[-3:] == '```':
        return 'CODE'
    # Quote
    if block[0:2] == '> ':
        lines = block.splitlines()
        if all(line[0:2] == '> ' for line in lines):
            return 'QUOTE'
    # Unordered list
    if (block[0:2] == '* ') or (block[0:2] == '- '):
        lines = block.splitlines()
        if all((line[0:2] == '* ' or line[0:2] == '- ') for line in lines):
            return 'UNORDERED_LIST'
    # Ordered list
    if block[0:3] == '1. ':
        lines = block.splitlines()
        pairs = list(enumerate(lines, start=1))
        # Why doesn't this conditional break out to the else block?
        if all(pair[1][0:3] == f'{pair[0]}. ' for pair in pairs):
            return 'ORDERED_LIST'
        else:
            return 'PARAGRAPH'
    else:
        return 'PARAGRAPH'
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match block_to_block_type(block):
            case 'HEADING':
                pass
            case 'QUOTE':
                pass
            case 'UNORDERED_LIST':
                pass
            case 'ORDERED_LIST':
                pass
            case 'PARAGRAPH':
                pass


if __name__ == '__main__':
    text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
    # text = " and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    blocks = markdown_to_blocks(text)
    for idx, block in enumerate(blocks, 1):
        print(f'Block {idx}:')
        print(block)
        print()