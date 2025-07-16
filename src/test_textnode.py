import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()
