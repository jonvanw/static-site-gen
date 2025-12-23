class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props = map(lambda item: f'{item[0]}="{item[1]}"', self.props.items())
        return " ".join(props)
    
    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None: 
            raise ValueError("LeafNode.value cannot be None")
        
        if self.tag is None:
            return self.value
        
        props = self.props_to_html()
        if len(props) > 1:
            props = " " + props
        return f'<{self.tag}{props}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode.tag cannot be None")
        
        if not self.children:
            raise ValueError("ParentNode must have children")
        
        children_html = "".join(map(lambda child: child.to_html(), self.children))
        props = self.props_to_html()
        if len(props) > 1:
            props = " " + props
        return f'<{self.tag}{props}>{children_html}</{self.tag}>'
