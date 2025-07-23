class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props_html = ""
        
        if self.props is None:
            return ""
        
        for (key, value) in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html
    
    def __repr__(self):
        return f'\nHTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("must have a text value")
        
        if self.tag == "a":
            if self.props is None:
                raise ValueError('"a" tag requires "href": "url"')
            return f'<a href="{self.props["href"]}">{self.value}</a>'
                
        if self.tag is None:
            return f'{self.value}'
        
        return f'<{self.tag}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'\nLeafNode({self.tag}, {self.value}, {self.props})'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        child_html = ""
        
        if self.tag is None:
            raise ValueError("must have a tag")

        if self.children is None:
            raise ValueError("must have a child")

        for child in self.children:
            child_html += child.to_html()

        return f'<{self.tag}>{child_html}</{self.tag}>'

    def __repr__(self):
        return f'\nParentNode({self.tag}, {self.children}, {self.props})'
  