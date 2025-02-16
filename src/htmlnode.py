class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        if children is not None:
            self.children = children[:]
        else:
            self.children = children
        if props is not None:
            self.props = props.copy()
        else:
            self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not isinstance(self.props, dict):
            return ''
        strings = [f' {key}="{value}"' for key, value in self.props.items()]
        return ''.join(strings)
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError('LeafNode.value should not be None')
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('ParentNode.tag should not be None')
        if (self.children is None) or (len(self.children) == 0):
            raise ValueError('ParentNode.children should not be empty')

        html_strings = [child.to_html() for child in self.children]
        formatted_html = ''.join(html_strings)

        return f'<{self.tag}>{formatted_html}</{self.tag}>'