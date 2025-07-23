from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_to_text import extract_markdown_images, extract_markdown_links, text_to_textnodes


def main():
    text = "curfuffle"
    text2 = "flercuffle"
    text_type = TextType.LINK
    child = ["list"]
    prop = {"dict": "yes"}
    url = "https://www.noonerfloofer.com"
    image_text = "This is text with  a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    image_empty = "This is text with no image"
    full_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    test_textnode = TextNode(text, text_type, url)
    test_htmlnode = HTMLNode(text, text2, child, prop)
    test_leafnode = LeafNode(text, text2, prop)
    test_parentnode = ParentNode(text, child, prop)
    test_image_extract = extract_markdown_images(image_text)
    test_link_extract = extract_markdown_links(link_text)
    test_image_extract_empty = extract_markdown_images(image_empty)
    test_full= text_to_textnodes(full_text)

    print(test_textnode)
    print(test_htmlnode)
    print(test_leafnode)
    print(test_parentnode)
    print(test_image_extract)
    print(test_link_extract)
    print(test_image_extract_empty)
    print(full_test)


if __name__ == "__main__":
    main()