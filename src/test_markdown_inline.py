import unittest

from textnode import TextNode, TextType
from markdown_inline import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes
)


class TestMarkdownToText(unittest.TestCase):
    def test_eq_delimiter_split(self):
        old_node = [TextNode("This is a text node with a **bold block** of words", TextType.TEXT)]
        new_with_bold = split_nodes_delimiter(old_node, "**", TextType.BOLD)

        self.assertEqual(new_with_bold,
            [TextNode("This is a text node with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" of words", TextType.TEXT)
            ]
        )

    def test_no_delimiter_split(self):
        old_node = [TextNode("This is a text node with no delimiter", TextType.TEXT)]
        new_only_text = split_nodes_delimiter(old_node, "_", TextType.ITALIC)

        self.assertEqual(new_only_text, [TextNode("This is a text node with no delimiter", TextType.TEXT)])
        
    def test_eq_multiple_delimiter(self):
        old_nodes = [
            TextNode("This is a text node with a **bold block** of words", TextType.TEXT),
            TextNode("This is a text node with an _italic block_ of words", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(new_nodes,
            [TextNode("This is a text node with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" of words", TextType.TEXT),
            TextNode("This is a text node with an _italic block_ of words", TextType.TEXT)
            ]
        )

    def test_bypass_delimiter(self):
        old_node = [TextNode("This should be a **bypassed** node", TextType.BOLD)]
        new_node = split_nodes_delimiter(old_node, "**", TextType.BOLD)

        self.assertEqual(new_node,  [TextNode("This should be a **bypassed** node", TextType.BOLD)])

    def test_missing_delimit_error(self):
        old_node = [TextNode("This is missing **one delimiter", TextType.TEXT)]
        
        with self.assertRaises(Exception) as exc:
            new_node = split_nodes_delimiter(old_node, "**", TextType.BOLD)
        self.assertEqual(f'{exc.exception}', "missing closing delimiter")

    def test_extract_markdown_images(self):
        images = extract_markdown_images(
            "This is text with an ![image](https://www.floofernooner.com)"
            "and another ![image2](https://www.curfufflefluffle.com)"
            "and another ![image3](https://www.shuttlebuttle.com)"
        )
        self.assertListEqual([
            ("image", "https://www.floofernooner.com"),
            ("image2", "https://www.curfufflefluffle.com"),
            ("image3", "https://www.shuttlebuttle.com")
            ], images
        )
    
    def test_extract_markdown_links(self):
        links = extract_markdown_links(
            "This is text with a link[floofed](https://www.floofernooner.com)"
            "and another [fluffled](https://www.curfufflefluffle.com)"
            "and another [buttled](https://www.shuttlebuttle.com)"
        )
        self.assertListEqual([
            ("floofed", "https://www.floofernooner.com"),
            ("fluffled", "https://www.curfufflefluffle.com"),
            ("buttled", "https://www.shuttlebuttle.com")
            ], links
        )

    def test_eq_image_split(self):
        old_node = [
            TextNode("This is a node with an ![image](https://www.floofernooner.com/image.png) embedded", 
            TextType.TEXT
            )
        ]
        new_nodes = split_nodes_image(old_node)

        self.assertEqual(new_nodes,
            [TextNode("This is a node with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://www.floofernooner.com/image.png"),
            TextNode(" embedded", TextType.TEXT)
            ]
        )

    def test_eq_image_multiple(self):
        old_node = [
            TextNode("This is a node with two "
            "![image1](https://www.floofernooner.com/image1.png) images "
            "![image2](https://www.floofernooner.com/image2.png) embedded",
            TextType.TEXT
            )
        ]
        new_nodes = split_nodes_image(old_node)

        self.assertEqual(new_nodes,
            [TextNode("This is a node with two ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "https://www.floofernooner.com/image1.png"),
            TextNode(" images ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://www.floofernooner.com/image2.png"),
            TextNode(" embedded", TextType.TEXT)
            ]
        )

    def test_no_image_split(self):
        old_node = [TextNode("This is text with no image", TextType.TEXT)]
        new_node = split_nodes_image(old_node)
        
        self.assertEqual(new_node, [TextNode("This is text with no image", TextType.TEXT)])

    def test_no_image_multiple(self):
        old_node = [
            TextNode("This is text with no image", TextType.TEXT),
            TextNode("This is text2 with no image", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_node)

        self.assertEqual(new_nodes, [
            TextNode("This is text with no image", TextType.TEXT),
            TextNode("This is text2 with no image", TextType.TEXT)
            ]
        )

    def test_bypass_image_split(self):
        old_node = [TextNode("**This is text with bold text**", TextType.BOLD)]
        new_node = split_nodes_image(old_node)

        self.assertEqual(new_node, [TextNode("**This is text with bold text**", TextType.BOLD)])

    def test_eq_link_split(self):
        old_node = [
            TextNode("This is a node with a [link](https://www.floofernooner.com/) embedded", 
            TextType.TEXT
            )
        ]
        new_nodes = split_nodes_link(old_node)

        self.assertEqual(new_nodes,
            [TextNode("This is a node with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.floofernooner.com/"),
            TextNode(" embedded", TextType.TEXT)
            ]
        )
    
    def test_eq_link_multiple(self):
        old_node = [
            TextNode("This is a node with two "
            "[link1](https://www.floofernooner1.com/) links "
            "[link2](https://www.floofernooner2.com/) embedded",
            TextType.TEXT
            )
        ]
        new_nodes = split_nodes_link(old_node)

        self.assertEqual(new_nodes,
            [TextNode("This is a node with two ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://www.floofernooner1.com/"),
            TextNode(" links ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://www.floofernooner2.com/"),
            TextNode(" embedded", TextType.TEXT)
            ]
        )
    
    def test_no_link_split(self):
        old_node = [TextNode("This is text with no link", TextType.TEXT)]
        new_node = split_nodes_link(old_node)
        
        self.assertEqual(new_node, [TextNode("This is text with no link", TextType.TEXT)])

    def test_no_link_multiple(self):
        old_node = [
            TextNode("This is text with no link", TextType.TEXT),
            TextNode("This is text2 with no link", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_node)

        self.assertEqual(new_nodes, [
            TextNode("This is text with no link", TextType.TEXT),
            TextNode("This is text2 with no link", TextType.TEXT)
            ]
        )

    def test_bypass_link_split(self):
        old_node = [TextNode("**This is text with bold text**", TextType.BOLD)]
        new_node = split_nodes_link(old_node)

        self.assertEqual(new_node, [TextNode("**This is text with bold text**", TextType.BOLD)])

    def test_eq_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertEqual(new_nodes,
            [TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
            ]
        )


if __name__ == "__main__":
    unittest.main()