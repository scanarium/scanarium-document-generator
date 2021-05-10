from .environment import DocumentPageTestCase
from document_generator import MarkdownRenderer


class MarkdownRendererTest(DocumentPageTestCase):
    def assertRendered(self, input, expected):
        renderer = MarkdownRenderer()
        actual = renderer.render(input)
        self.assertEqual(actual, expected)

    def test_simple(self):
        self.assertRendered('# Foo', '<h1>Foo</h1>')
