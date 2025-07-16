import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_arg_eq(self):
        node = HTMLNode(
            "this is a tag", 
            "this is a value", 
            ["this is a child list"],
            {"this is a props": "dict"}
        )
        
        self.assertEqual(node.tag, "this is a tag")
        self.assertEqual(node.value, "this is a value")
        self.assertEqual(node.children, ["this is a child list"])
        self.assertEqual(node.props, {"this is a props": "dict"})

    def test_props_to_html(self):
        node = HTMLNode(
            "this is a tag", 
            "this is a value", 
            ["this is a child list"],
            {"this is a props": "dict"}
        )

        self.assertEqual(node.props_to_html(), ' this is a props="dict"')

    def test_arg_not_eq(self):
        node = HTMLNode("this is a tag")
        node2 = HTMLNode("this is a tag2")
        
        self.assertNotEqual(node, node2)
    
    def test_arg_none(self):
        node = HTMLNode()
        
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        node = HTMLNode(
            "tag here", 
            "value here", 
            ["child list"],
            {"props": "dict"}
        )

        self.assertEqual(
            node.__repr__(), 
            "HTMLNode(tag here, value here, ['child list'], {'props': 'dict'})"
        )       


if __name__ == "__main__":
    unittest.main()
       