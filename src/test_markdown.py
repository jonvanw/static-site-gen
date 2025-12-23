import unittest

from markdown import split_nodes_delimiter
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

if __name__ == "__main__":
    unittest.main()    