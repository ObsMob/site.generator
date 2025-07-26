import unittest
import textwrap

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from markdown_blocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    is_list_type,
    is_code_type,
    is_heading_type,
    is_quote_type,
    block_to_textnodes,
    block_textnode_to_htmlnode,
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_eq_markdown_to_blocks(self):
        md = textwrap.dedent("""\
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        )
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown_to_blocks(self):
        md = ""
        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, [])

    def test_block_type_head(self):
        md = textwrap.dedent("""\
            # Heading 1

            ## Heading 2

            ### Heading 3
            """
        )
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEAD)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.HEAD)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.HEAD)
        self.assertEqual(is_heading_type(blocks[0]), True)
        self.assertEqual(is_heading_type(blocks[1]), True)
        self.assertEqual(is_heading_type(blocks[2]), True)

    def test_block_type_code(self):
        block = "```This is a code block```"

        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        self.assertEqual(is_code_type(block), True)
        self.assertEqual(
            block_to_textnodes(block),
            [TextNode("This is a code block", TextType.CODE)]
        )

    def test_block_type_quote(self):
        md = textwrap.dedent("""\
            >This is text
            >from a 
            >long quote

            >This is a new quote
            """
        )
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.QUOTE)

    def test_block_type_bullet(self):
        md = textwrap.dedent("""\
            - Bullet list item 1
            - Bullet list item 2
            - Bullet list item 3

            - Bullet list 2
            """
        )
        blocks = markdown_to_blocks(md)
        text_node1 = block_to_textnodes(blocks[0])
        text_node2 = block_to_textnodes(blocks[1])

        
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.BULLET)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.BULLET)
        self.assertEqual(is_list_type(blocks[0]), True)
        self.assertEqual(is_list_type(blocks[1]), True)
        self.assertEqual(block_textnode_to_htmlnode(text_node2, blocks[1]),
            [ParentNode("li", [LeafNode(None, "Bullet list 2")])]
        )
        self.assertEqual(block_textnode_to_htmlnode(text_node1, blocks[0]),
            [
            ParentNode("li", [LeafNode(None, "Bullet list item 1")]),
            ParentNode("li", [LeafNode(None, "Bullet list item 2")]),
            ParentNode("li", [LeafNode(None, "Bullet list item 3")])
            ]
        )

    def test_block_type_numbered(self):
        md = textwrap.dedent("""\
            1. This is
            2. an ordered
            3. list

            1. New ordered list
            """
        )
        blocks = markdown_to_blocks(md)
        text_node1 = block_to_textnodes(blocks[0])
        text_node2 = block_to_textnodes(blocks[1])
        
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.NUMBER)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.NUMBER)
        self.assertEqual(is_list_type(blocks[0]), True)
        self.assertEqual(is_list_type(blocks[1]), True)
        self.assertEqual(block_textnode_to_htmlnode(text_node2, blocks[1]),
            [ParentNode("li", [LeafNode(None, "New ordered list")])]
        )
        self.assertEqual(block_textnode_to_htmlnode(text_node1, blocks[0]),
            [
            ParentNode("li", [LeafNode(None, "This is")]),
            ParentNode("li", [LeafNode(None, "an ordered")]),
            ParentNode("li", [LeafNode(None, "list")])
            ]
        )

    def test_block_type_paragraph(self):
        block = "this is a paragraph block"

        self.assertEqual(block_to_block_type(block), BlockType.PGRAPH)

    def test_block_type_errors(self):
        md = textwrap.dedent("""\
            ```This is an unclosed code block

            -This is an unordered list without a space

            1.This is an ordered list without a space
            """
        )
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PGRAPH)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PGRAPH)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.PGRAPH)

    def test_markdown_to_html(self):
        md = textwrap.dedent("""\
            # This is heading 1

            ### This is heading 3
        
            >This is
            >a multi-line
            >quote block

            1. This is an
            2. ordered list block

            - This is an
            - unordered list block

            ```This **is** a _code_ block```

            This is a **standard** paragraph _block_ with an ![image](http://www.floofer.com)
            and a [link](http://www.obsmob.com).
            """
        )

        html_node = markdown_to_html_node(md)

        #print(html_node.to_html())
        self.assertEqual(html_node.to_html(),
            "<div><h1>This is heading 1</h1><h3>This is heading 3</h3>"
            "<blockquote>This is a multi-line quote block</blockquote>"
            "<ol><li>This is an</li><li>ordered list block</li></ol>"
            "<ul><li>This is an</li><li>unordered list block</li></ul>"
            "<pre><code>This **is** a _code_ block</code></pre>"
            "<p>This is a <b>standard</b> paragraph <i>block</i>"
            ' with an <img src="http://www.floofer.com" alt="image">'
            'and a <a href="http://www.obsmob.com">link</a>.</p></div>'
        )


if __name__ == "__main__":
    unittest.main()  