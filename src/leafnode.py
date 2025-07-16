from htmlnode import HTMLNode


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
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
 