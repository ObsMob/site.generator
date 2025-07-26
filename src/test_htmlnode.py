import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
            "\nHTMLNode(tag here, value here, ['child list'], {'props': 'dict'})"
        )       

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
        node3 = LeafNode("img", "", {"src": "obsmob.com", "alt": "this is alt text"})
        
        self.assertEqual(node.to_html(), "<b>this is bold text</b>")
        self.assertEqual(node2.to_html(), '<a href="obsmob.com">this is link text</a>')
        self.assertEqual(node3.to_html(), '<img src="obsmob.com" alt="this is alt text">')

    def test_to_html_error(self):
        node = LeafNode("a", "this is link text")
        node2 = LeafNode(None, None)

        with self.assertRaises(ValueError) as exc:
            node.to_html()
        self.assertEqual(f'{exc.exception}', '"a" and "img" tags require a "url"')

        with self.assertRaises(ValueError) as exc2:
            node2.to_html()
        self.assertEqual(f'{exc2.exception}', "must have a text value")

    def test_arg_not_eq(self):
        node = LeafNode(None, "this is a value")
        node2 = LeafNode(None, "this is a value2")
        
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
            "\nLeafNode(tag first, value second, {'props': 'dict'})"
        )

class TestParentNode(unittest.TestCase):
    def test_arg_eq(self):
        node = ParentNode(
            "this is a tag",  
            ["this is a child list"],
            {"this is a props": "dict"}
        )

        self.assertEqual(node.tag, "this is a tag")
        self.assertEqual(node.children, ["this is a child list"])
        self.assertEqual(node.props, {"this is a props": "dict"})

    def test_arg_not_eq(self):
        node = ParentNode("this is a tag", ["this is a list"])
        node2 = ParentNode("this is a tag2", ["this is a list"])
        node3 = ParentNode("this is a tag", ["this is a list2"])
        
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)

    def test_to_html(self):
        child1 = LeafNode("b", "child 1 BOLD")
        child2 = LeafNode("i", "child 2 ITALIC")
        child3 = LeafNode("u", "child 3 UNDERLINE")
        child4 = LeafNode("c", "child 4 CURSIVE")
        parent1 = ParentNode("p1", [child1, child2])
        parent2 = ParentNode("p2", [child3, child4])
        grandparent = ParentNode("h", [parent1, parent2])

        self.assertEqual(parent1.to_html(),
            "<p1><b>child 1 BOLD</b><i>child 2 ITALIC</i></p1>"
        )
        self.assertEqual(parent2.to_html(),
            "<p2><u>child 3 UNDERLINE</u><c>child 4 CURSIVE</c></p2>"
        )
        self.assertEqual(grandparent.to_html(),
            "<h><p1><b>child 1 BOLD</b><i>child 2 ITALIC</i></p1><p2><u>child 3 UNDERLINE</u><c>child 4 CURSIVE</c></p2></h>"
        )

    def test_to_html_error(self):
        node = ParentNode(None, ["this is a list"])
        node2 = ParentNode("this is a tag", None)

        with self.assertRaises(ValueError) as exc:
            node.to_html()
        self.assertEqual(f'{exc.exception}', "must have a tag")

        with self.assertRaises(ValueError) as exc2:
            node2.to_html()
        self.assertEqual(f'{exc2.exception}', "must have a child")

    def test_arg_none(self):
        node = ParentNode("this is a tag", ["this is a list"])
        
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)

    def test_repr(self):
        node = ParentNode(
            "tag first",
            ["child list second"], 
            {"props": "dict"}
        )

        self.assertEqual(
            node.__repr__(), 
            "\nParentNode(tag first, ['child list second'], {'props': 'dict'})"
        )


if __name__ == "__main__":
    unittest.main()       