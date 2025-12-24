import re
from textnode import TextNode, TextType

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