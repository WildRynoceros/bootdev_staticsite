import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq_1(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("This is a link node", TextType.LINK, url='google.com')
        node2 = TextNode("This is a link node", TextType.LINK, url='google.com')
        self.assertEqual(node, node2)

    def test_neq_1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT, url='yay')
        self.assertNotEqual(node, node2)

class Test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode('TEST', TextType.TEXT)
        leaf = text_node_to_html_node(node)
        self.assertIsNone(leaf.tag)
        self.assertEqual(leaf.value, 'TEST')

    def test_bold(self):
        node = TextNode('TEST', TextType.BOLD)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, 'b')
        self.assertEqual(leaf.value, 'TEST')

    def test_italic(self):
        node = TextNode('TEST', TextType.ITALIC)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, 'i')
        self.assertEqual(leaf.value, 'TEST')

    def test_code(self):
        node = TextNode('TEST', TextType.CODE)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, 'code')
        self.assertEqual(leaf.value, 'TEST')

    def test_link(self):
        node = TextNode('TEST', TextType.LINK, url='TEST')
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, 'a')
        self.assertEqual(leaf.value, 'TEST')
        self.assertDictEqual(leaf.props, {'href': 'TEST'})

    def test_image(self):
        node = TextNode('TEXT', TextType.IMAGE, url='URL')
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, 'img')
        self.assertEqual(leaf.value, '')
        self.assertDictEqual(leaf.props, {'src': 'URL', 'alt': 'TEXT'})

    def test_none(self):
        node = TextNode('TEXT', None)
        self.assertRaises(ValueError, text_node_to_html_node, node)

    def test_incorrect_text_type(self):
        node = TextNode('TEXT', 69420)
        self.assertRaises(ValueError, text_node_to_html_node, node)

class Test_text_node_to_html_node(unittest.TestCase):
    def test_bold(self):
        node = TextNode('This is text with a **bolded phrase** in the middle', TextType.TEXT)
        nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        
        self.assertEqual(len(nodes), 3)
        expected = [
            ('This is text with a ', TextType.TEXT), 
            ('bolded phrase', TextType.BOLD),
            (' in the middle', TextType.TEXT)
        ]
        for idx, expectation in enumerate(expected):
            self.assertEqual(expectation[0], nodes[idx].text)
            self.assertEqual(expectation[1], nodes[idx].text_type)

    def test_italic(self):
        node = TextNode('This is text with a *italicized phrase* in the middle', TextType.TEXT)
        nodes = split_nodes_delimiter([node], '*', TextType.ITALIC)
        
        self.assertEqual(len(nodes), 3)
        expected = [
            ('This is text with a ', TextType.TEXT), 
            ('italicized phrase', TextType.ITALIC),
            (' in the middle', TextType.TEXT)
        ]
        for idx, expectation in enumerate(expected):
            self.assertEqual(expectation[0], nodes[idx].text)
            self.assertEqual(expectation[1], nodes[idx].text_type)

    def test_code(self):
        node = TextNode('This is text with `code` in the middle', TextType.TEXT)
        nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        
        self.assertEqual(len(nodes), 3)
        expected = [
            ('This is text with ', TextType.TEXT), 
            ('code', TextType.CODE),
            (' in the middle', TextType.TEXT)
        ]
        for idx, expectation in enumerate(expected):
            self.assertEqual(expectation[0], nodes[idx].text)
            self.assertEqual(expectation[1], nodes[idx].text_type)

    def test_all(self):
        node = TextNode('This is text with **bold**, *italics*, and `code`', TextType.TEXT)
        nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
        
        self.assertEqual(len(nodes), 6)
        expected = [
            ('This is text with ', TextType.TEXT),
            ('bold', TextType.BOLD),
            (', ', TextType.TEXT),
            ('italics', TextType.ITALIC),
            (', and ', TextType.TEXT),
            ('code', TextType.CODE)
        ]
        for idx, expectation in enumerate(expected):
            self.assertEqual(expectation[0], nodes[idx].text)
            self.assertEqual(expectation[1], nodes[idx].text_type)
    
    def test_text_to_bold(self):
        node = TextNode('**THIS IS JUST BOLD**', TextType.TEXT)
        nodes = split_nodes_delimiter([node], '**', TextType.BOLD)

        self.assertEqual(len(nodes), 1)
        expected = [
            ('THIS IS JUST BOLD', TextType.BOLD)
        ]

        for idx, expectation in enumerate(expected):
            self.assertEqual(expectation[0], nodes[idx].text)
            self.assertEqual(expectation[1], nodes[idx].text_type)

class Test_extract_markdown_images(unittest.TestCase):
    def test_image_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_url_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(text)
        self.assertEqual(len(matches), 0)

class Test_extract_markdown_links(unittest.TestCase):
    def test_image_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(text)
        self.assertEqual(len(matches), 0)

    def test_url_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

class Test_split_nodes_link(unittest.TestCase):
    link_node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    image_node = TextNode(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
        TextType.TEXT
    )
    all_links_node = TextNode(
        "[oops](url1)[all](url2)[links!](url3)",
        TextType.TEXT
    )
    def test_only_links(self):
        created = split_nodes_link([Test_split_nodes_link.link_node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, url="https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(expected, created)

    def test_only_images(self):
        created = split_nodes_link([Test_split_nodes_link.image_node])
        expected = [
            Test_split_nodes_link.image_node
        ]
        self.assertEqual(expected, created)

    def test_link_and_image(self):
        created = split_nodes_link([Test_split_nodes_link.link_node, Test_split_nodes_link.image_node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, url="https://www.youtube.com/@bootdotdev"),
            Test_split_nodes_link.image_node
        ]
        self.assertEqual(expected, created)

    def test_only_links(self):
        created = split_nodes_link([Test_split_nodes_link.all_links_node])
        expected = [
            TextNode("oops", TextType.LINK, url='url1'),
            TextNode("all", TextType.LINK, url='url2'),
            TextNode("links!", TextType.LINK, url='url3')
        ]
        self.assertEqual(expected, created)

class Test_split_nodes_images(unittest.TestCase):
    link_node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    image_node = TextNode(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
        TextType.TEXT
    )
    all_images_node = TextNode(
        "![oops](url1)![all](url2)![images!](url3)",
        TextType.TEXT
    )
    def test_only_links(self):
        created = split_nodes_image([Test_split_nodes_link.link_node])
        expected = [
            Test_split_nodes_images.link_node
        ]
        self.assertEqual(expected, created)

    def test_only_images(self):
        created = split_nodes_image([Test_split_nodes_link.image_node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(expected, created)

    def test_link_and_image(self):
        created = split_nodes_image([Test_split_nodes_link.link_node, Test_split_nodes_link.image_node])
        expected = [
            Test_split_nodes_link.link_node,
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(expected, created)

    def test_only_links(self):
        created = split_nodes_image([Test_split_nodes_images.all_images_node])
        expected = [
            TextNode("oops", TextType.IMAGE, url='url1'),
            TextNode("all", TextType.IMAGE, url='url2'),
            TextNode("images!", TextType.IMAGE, url='url3')
        ]
        self.assertEqual(expected, created)

class Test_text_to_textnodes(unittest.TestCase):
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    def test_text_variety(self):
        created = text_to_textnodes(Test_text_to_textnodes.text)
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
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(expected, created)

class Test_markdown_to_blocks(unittest.TestCase):
    single_block = "This is a single block of text"
    multiple_block = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

    def test_single_block(self):
        created = markdown_to_blocks(Test_markdown_to_blocks.single_block)
        expected = ['This is a single block of text']
        self.assertEqual(expected, created)

    def test_multiple_block(self):
        created = markdown_to_blocks(Test_markdown_to_blocks.multiple_block)
        expected = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertEqual(expected, created)

if __name__ == "__main__":
    unittest.main()