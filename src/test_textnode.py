import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertEqual(node.text_type, node2.text_type)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.text, node2.text)
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
        self.assertEqual(node.url, None)

    def test_text_to_html(self):
        value = "This is a text node"
        node = TextNode(value, TextType.TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, value)

    def test_bold_to_html(self):
        value = "This is a bold text node"
        node = TextNode(value, TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, value)

    def test_bold_to_html(self):
        value = "This is an italics text node"
        node = TextNode(value, TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, value)

    def test_code_to_html(self):
        value = "This is a code text node"
        node = TextNode(value, TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, value)

    def test_link_to_html(self):
        value = "This is a link text node"
        url = "https://www.google.com"
        node = TextNode(value, TextType.LINK, url)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, value)
        self.assertDictEqual(html_node.props, {"href": url})

    def test_link_to_html(self):
        value = "This is a link text node"
        url = "https://www.google.com"
        node = TextNode(value, TextType.IMAGE, url)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertDictEqual(html_node.props, {"src": url, "alt": value})

if __name__ == "__main__":
    unittest.main()