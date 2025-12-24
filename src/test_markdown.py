import unittest

from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(expected, new_nodes)

    def test_split_nodes_bold(self):
        node = TextNode("This is text with **bolded text!**", TextType.TEXT)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bolded text!", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(expected, new_nodes)

    def test_split_nodes_italics(self):
        node = TextNode("_This text is italics._ This text is not.", TextType.TEXT)
        expected = [
            TextNode("This text is italics.", TextType.ITALIC),
            TextNode(" This text is not.", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(expected, new_nodes)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        expected = [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ]
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(expected, new_nodes)

    def test_delim_unbalanced(self):
        node = TextNode("The _italics in this text is not closed", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        the_exception = cm.exception
        self.assertEqual('Encountered unpaired "_" delimiter in the following text: "The _italics in this text is not closed"', the_exception.args[0])

    def test_extract_md_images_multi(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        actual = extract_markdown_images(text)
        self.assertListEqual(expected, actual)

    def test_extract_md_images_single(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        actual = extract_markdown_images(text)
        self.assertListEqual(expected, actual)

    def test_extract_md_images_none(self):
        text = "This is text with any images. [this is not an image]. (nor is this)"
        expected = []
        actual = extract_markdown_images(text)
        self.assertListEqual(expected, actual)

    def test_extract_md_images_not_links(self):
        text = "This text contains [a link](https://www.google.com)"
        expected = []
        actual = extract_markdown_images(text)
        self.assertListEqual(expected, actual)

    def test_extract_md_link_single(self):
        text = "This text includes [a link](https://www.amazon.com)"
        expected = [('a link', 'https://www.amazon.com')]
        actual = extract_markdown_links(text)
        self.assertListEqual(expected, actual)

    def test_extract_md_link_multiple(self):
        text = "This text includes multiple links: [Japan](https://www.amazon.co.jp), [UK](https://www.amazon.co.uk)"
        expected = [('Japan', 'https://www.amazon.co.jp'), ('UK', 'https://www.amazon.co.uk')]
        actual = extract_markdown_links(text)
        self.assertListEqual(expected, actual)

    def test_extract_md_link_none(self):
        text = "This text does not include any links."
        expected = []
        actual = extract_markdown_links(text)
        self.assertListEqual(expected, actual)
    
    def test_extract_md_link_only_img(self):
        text = "This text only includes an image: ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = []
        actual = extract_markdown_links(text)
        self.assertListEqual(expected, actual)

    def test_extract_md_both_link_img(self):
        text = "This text includes [a link](https://www.amazon.com) and an image: ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected_link = [('a link', 'https://www.amazon.com')]
        expected_img = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        actual_link = extract_markdown_links(text)
        actual_img = extract_markdown_images(text)
        self.assertListEqual(expected_img, actual_img)
        self.assertListEqual(expected_link, actual_link)

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        actual = split_nodes_link([node])
        self.assertListEqual(expected, actual)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        expected = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ]
        actual = split_nodes_image([node])
        self.assertListEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()    