import unittest

from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links,\
      split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, \
      block_to_block_type, BlockType
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

    def test_text_to_textnodes(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertListEqual(expected, actual)

    def test_text_to_textnodes_empty(self):
        text = ""
        expected = []
        actual = text_to_textnodes(text)
        self.assertListEqual(expected, actual)

    def test_text_to_textnoodes_plaintext(self):
        text = "this is just some plain text."
        expected = [TextNode(text, TextType.TEXT)]
        actual = text_to_textnodes(text)
        self.assertListEqual(expected, actual)

    def test_text_to_textnoodes_bolded(self):
        text = "**this text is all bolded!**"
        expected = [TextNode("this text is all bolded!", TextType.BOLD)]
        actual = text_to_textnodes(text)
        self.assertListEqual(expected, actual)

    def test_text_to_textnoodes_image_only(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
        actual = text_to_textnodes(text)
        self.assertListEqual(expected, actual)

    def test_markdown_to_blocks_multiple_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        actual = markdown_to_blocks(md)
        self.assertEqual(expected, actual)

    def test_markdown_to_blocks_single_block(self):
        md = """
This block of text spans multiple lines but
is considered a single block because there are no empty lines between.

"""

        expected = ["This block of text spans multiple lines but\nis considered a single block because there are no empty lines between."]
        actual = markdown_to_blocks(md)
        self.assertListEqual(expected, actual)

    def test_markdown_to_blocks_no_blocks(self):
        md = """


"""
        expected = []
        actual = markdown_to_blocks(md)

        self.assertListEqual(expected, actual)


    def test_block_to_type_paragraph(self):
        block = "Plaintext without any special characters is treated as a basic paragraph.\nEven if it spans multiple lines."

        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_type_heading(self):
        block = "# Headings start with a hash symbol (#)."

        result = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, result)

    def test_block_to_type_code(self):
        block = "```This is a code block\nbecause its surrounded by triple-backtick characters (```).```"

        result = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, result)

    def test_block_to_type_heading(self):
        block = "> Quotes start with the greater than symbol (>)."

        result = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, result)

    def test_block_to_type_unordered_single_item(self):
        block = "- this is a single item unordered list."

        result = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, result)

    def test_block_to_type_unordered_multi_item(self):
        block = "- this is an unordered list.\n - with multiple items."

        result = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, result)

    def test_block_to_type_ordered_single_item(self):
        block = " 0. note that ordered lists don't always start at 1."

        result = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, result)

    def test_block_to_type_ordered_multi_item(self):
        block = "1. this is an unordered list.\n 2. with multiple items."

        result = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, result)  

if __name__ == "__main__":
    unittest.main()    