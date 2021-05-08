from .environment import HelpPageTestCase
from help_generator import MarkdownRenderer


class MarkdownRendererTest(HelpPageTestCase):
    def assertRendered(self, input, expected):
        renderer = MarkdownRenderer()
        actual = renderer.render(input)
        self.assertEqual(actual, expected)

    def test_simple(self):
        self.assertRendered('# Foo', '<h1>Foo</h1>')
