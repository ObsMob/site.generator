import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_arg_eq(self):
        node = LeafNode( 
            "this is a tag",
            "this is a value", 
            {"this is a props": "dict"}
        )
        
        self.assertEqual(node.tag, "this is a tag")        
        self.assertEqual(node.value, "this is a value")
        self.assertEqual(node.props, {"this is a props": "dict"})

    def test_to_html(self):
        node = LeafNode("b", "this is bold text")
        node2 = LeafNode("a", "this is link text", {"href": "obsmob.com"})
        
        self.assertEqual(node.to_html(), "<b>this is bold text</b>")
        self.assertEqual(node2.to_html(), '<a href="obsmob.com">this is link text</a>')

    def test_to_html_error(self):
        node = LeafNode("a", "this is link text")
        node2 = LeafNode(None, None)

        with self.assertRaises(ValueError) as exc:
            node.to_html()
        self.assertEqual(f'{exc.exception}', '"a" tag requires "href": "url"')

        with self.assertRaises(ValueError) as exc2:
            node2.to_html()
        self.assertEqual(f'{exc2.exception}', "must have a text value")

    def test_arg_not_eq(self):
        node = LeafNode(None, "this is a tag")
        node2 = LeafNode(None, "this is a tag2")
        
        self.assertNotEqual(node, node2)
    
    def test_arg_none(self):
        node = LeafNode(None, "must have value")
        
        self.assertIsNone(node.tag)
        self.assertIsNone(node.props)

    def test_repr(self):
        node = LeafNode(
            "tag first",
            "value second", 
            {"props": "dict"}
        )

        self.assertEqual(
            node.__repr__(), 
            "LeafNode(tag first, value second, {'props': 'dict'})"
        )       


if __name__ == "__main__":
    unittest.main()
  