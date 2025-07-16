from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():
    text = "curfuffle"
    text2 = "flercuffle"
    linkz = TextType.LINK
    child = ["list"]
    prop = {"dict": "yes"}
    url = "https://www.noonerfloofer.com"
    test_textnode = TextNode(text, linkz, url)
    test_htmlnode = HTMLNode(text, text2, child, prop)
    print(test_textnode)
    print(test_htmlnode.__repr__())

main()
