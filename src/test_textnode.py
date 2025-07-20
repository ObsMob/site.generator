import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
                
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)

        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)

        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.LINK)

        self.assertIsNone(node.url)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.noonerfloofer.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.noonerfloofer.com")
        
        self.assertEqual(node.url, node2.url)

class TestTextToHTML(unittest.TestCase):
    def test_text_to_html(self):
        node_text = TextNode("This is a text node", TextType.TEXT)
        html_text = text_node_to_html_node(node_text)
        node_bold = TextNode("This is a bold node", TextType.BOLD)
        html_bold = text_node_to_html_node(node_bold)
        node_italic = TextNode("This is an italic node", TextType.ITALIC)
        html_italic = text_node_to_html_node(node_italic)
        node_code = TextNode("This is a code node", TextType.CODE)
        html_code = text_node_to_html_node(node_code)
        
        self.assertEqual(html_text.tag, None)
        self.assertEqual(html_text.value, "This is a text node")
        self.assertEqual(html_bold.tag, "b")
        self.assertEqual(html_bold.value, "This is a bold node")
        self.assertEqual(html_italic.tag, "i")
        self.assertEqual(html_italic.value, "This is an italic node")
        self.assertEqual(html_code.tag, "code")
        self.assertEqual(html_code.value, "This is a code node")

    def test_text_to_html_link(self):
        node_link = TextNode("This is a link node", TextType.LINK, "http://www.link.com")
        html_link = text_node_to_html_node(node_link)
        
        self.assertEqual(html_link.tag, "a")
        self.assertEqual(html_link.value, "This is a link node")
        self.assertEqual(html_link.props, {"href": "http://www.link.com"})

    def test_text_to_html_img(self):
        node_img = TextNode("This is an img node", TextType.IMAGE, "http://www.img.com")
        html_img = text_node_to_html_node(node_img)
        
        self.assertEqual(html_img.tag, "img")
        self.assertEqual(html_img.value, "")  
        self.assertEqual(html_img.props,
            {"src": "http://www.img.com",
            "alt": "This is an img node"
            }
        )


if __name__ == "__main__":
    unittest.main()