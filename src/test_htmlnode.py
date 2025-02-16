import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init_default(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_filled(self):
        node = HTMLNode(tag='p', value='This is a p tag')
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'This is a p tag')
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props=dict())
        self.assertEqual(node.props_to_html(), '')

class TestLeafNode(unittest.TestCase):
    def test_init_default(self):
        self.assertRaises(TypeError, LeafNode)

    def test_init_filled_no_props(self):
        node = LeafNode('p', 'This is a p tag')
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'This is a p tag')
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_filled_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.tag, 'a')
        self.assertEqual(node.value, 'Click me!')
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"href": "https://www.google.com"})

    def test_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_init_default(self):
        self.assertRaises(TypeError, ParentNode)

    def test_init_filled_no_props(self):
        leaves = [
            LeafNode('b', 'Bold'),
            LeafNode(None, 'Normal'),
            LeafNode('i', 'Italic'),
            LeafNode(None, 'Normal text')
        ]
        node = ParentNode('p', leaves)

        self.assertEqual(node.tag, 'p')
        for idx, child in enumerate(node.children):
            self.assertEqual(child, leaves[idx])
        self.assertIsNone(node.props)

    def test_init_filled_props(self):
        leaves = [
            LeafNode('b', 'Bold'),
            LeafNode(None, 'Normal'),
            LeafNode('i', 'Italic'),
            LeafNode(None, 'Normal text')
        ]
        props = {'href': 'google.com'}
        node = ParentNode('a', leaves, props=props)

        self.assertEqual(node.tag, 'a')
        for idx, child in enumerate(node.children):
            self.assertEqual(child, leaves[idx])
        self.assertDictEqual(node.props, props)

    def test_to_html_no_tag_no_children(self):
        node = ParentNode(tag=None, children=None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(
            'ParentNode.tag should not be None',
            str(cm.exception)
        )

    def test_to_html_no_tag(self):
        leaves = [
            LeafNode('b', 'Bold'),
            LeafNode(None, 'Normal'),
            LeafNode('i', 'Italic'),
            LeafNode(None, 'Normal text')
        ]
        node = ParentNode(tag=None, children=leaves)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(
            'ParentNode.tag should not be None',
            str(cm.exception)
        )

    def test_to_html_no_children(self):
        node = ParentNode(tag='a', children=None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(
            'ParentNode.children should not be empty',
            str(cm.exception)
        )

    def test_to_html_1_leaf(self):
        leaves = [
            LeafNode('b', 'Bold'),
        ]
        node = ParentNode(tag='TEST', children=leaves)
        self.assertEqual(
            '<TEST><b>Bold</b></TEST>',
            node.to_html()
        )
    
    def test_to_html_many_leaves(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
            node.to_html()
        )
    
    def test_to_html_nested_parent(self):
        inner_parent = ParentNode(
            "INNER PARENT",
            [
                LeafNode("INNER CHILD 1", "1"),
                LeafNode("INNER CHILD 2", "2"),
            ],
        )
        outer_parent = ParentNode(
            "OUTER PARENT",
            [
                LeafNode('OUTER CHILD 1', '1'),
                inner_parent
            ]
        )
        self.assertEqual(
            '<OUTER PARENT><OUTER CHILD 1>1</OUTER CHILD 1><INNER PARENT><INNER CHILD 1>1</INNER CHILD 1><INNER CHILD 2>2</INNER CHILD 2></INNER PARENT></OUTER PARENT>',
            outer_parent.to_html()
        )