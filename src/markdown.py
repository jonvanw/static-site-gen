import re
from enum import Enum
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for old_node in old_nodes:
        parts = old_node.text.split(delimiter)
        inside = True
        for part in parts:
            inside = not inside
            new_type = text_type if inside else old_node.text_type
            new_node = TextNode(part, new_type)
            if part != "":
                nodes.append(new_node)
            

        if inside:
            raise Exception(f'Encountered unpaired "{delimiter}" delimiter in the following text: "{old_node.text}"')
    return nodes

def split_nodes_url_helper(old_nodes, replaced_text, text, text_type, url):
    if not url:
        raise ValueError('url must be specified')
    nodes = []
    for old_node in old_nodes:
        if old_node.url != None:
            nodes.append(old_node)
            continue
        parts = old_node.text.split(replaced_text)
        is_first_time = True
        for part in parts:
            if is_first_time:
                is_first_time = False
            else:
                url_node = TextNode(text, text_type, url)
                nodes.append(url_node)
            
            if part != "":
                new_node = TextNode(part, old_node.text_type)
                nodes.append(new_node)

    return nodes

def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
        current_nodes = [old_node]
        for image in images:
            current_nodes = \
                split_nodes_url_helper(current_nodes,
                    f'![{image[0]}]({image[1]})',
                    image[0], 
                    TextType.IMAGE,
                    image[1])
        new_nodes.extend(current_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        current_nodes = [old_node]
        for link in links:
            current_nodes = \
                split_nodes_url_helper(current_nodes,
                    f'[{link[0]}]({link[1]})',
                    link[0], 
                    TextType.LINK,
                    link[1])
        new_nodes.extend(current_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    lines = markdown.splitlines()
    blocks = []
    current_block = ""
    isNewBlock = True
    for line in lines:
        line = line.strip()
        if line == "":
            if current_block != "":
                blocks.append(current_block)
                current_block = ""
            isNewBlock = True
        else:
            current_block += line if isNewBlock else f'\n{line}'
            isNewBlock = False
    
    if current_block != "":
        blocks.append(current_block)

    return blocks

def block_to_block_type(block):
    block = block.strip()
    if block.startswith("#"):
        return BlockType.HEADING
    if block.startswith(">"):
        return BlockType.QUOTE
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.splitlines()
    lines = list(map(lambda line: line.strip(), lines))
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    numbered_pattern = r'^\d+.'
    if all(re.search(numbered_pattern, line) for line in lines):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    
