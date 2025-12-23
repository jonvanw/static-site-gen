import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        tag = "test_tag"
        value = "test_value"
        children = []
        props = {"href": "https://www.google.com", "target": "_blank"}
        sut = HTMLNode(tag, value, children, props)
        self.assertEqual(tag, sut.tag)
        self.assertEqual(value, sut.value)
        self.assertListEqual(children, sut.children)
        self.assertDictEqual(props, sut.props)

    def test_empty_constructor(self):
        sut = HTMLNode()
        self.assertEqual(None, sut.tag)
        self.assertEqual(None, sut.value)
        self.assertEqual(None, sut.children)
        self.assertEqual(None, sut.props)

    def test_props_to_html(self):
        tag = "test_tag"
        value = "test_value"
        children = []
        props = {"href": "https://www.google.com", "target": "_blank"}
        sut = HTMLNode(tag, value, children, props)
        actual_html = sut.props_to_html()
        expected_html = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(expected_html, actual_html)

    def test_leaf_to_html_no_tag(self):
        value = "test text"
        node = LeafNode(None, value)
        self.assertEqual(value, node.to_html())
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_nested_p(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        actual_html = node.to_html()
        expected_html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'

        self.assertEqual(expected_html, actual_html)

    def test_to_html_parent_no_tag(self):
        child_node = LeafNode("span", "child")
        node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_parent_no_child(self):
        node_children_empty = ParentNode("a", [])
        node_children_none = ParentNode("a", None)
        self.assertRaises(ValueError, node_children_empty.to_html)
        self.assertRaises(ValueError, node_children_none.to_html)

if __name__ == "__main__":
    unittest.main()