from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    text = "curfuffle"
    text2 = "flercuffle"
    text_type = TextType.LINK
    child = ["list"]
    prop = {"dict": "yes"}
    url = "https://www.noonerfloofer.com"
    test_textnode = TextNode(text, text_type, url)
    test_htmlnode = HTMLNode(text, text2, child, prop)
    test_leafnode = LeafNode(text, text2, prop)
    test_parentnode = ParentNode(text, child, prop)
    
    print(test_textnode)
    print(test_htmlnode)
    print(test_leafnode)
    print(test_parentnode)


if __name__ == "__main__":
    main()