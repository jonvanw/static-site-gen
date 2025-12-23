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