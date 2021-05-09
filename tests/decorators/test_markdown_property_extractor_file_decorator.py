from tests import HelpPageTestCase
from help_generator.decorators import MarkdownPropertyExtractorFileDecorator


class MarkdownPropertyExtractorFileDecoratorTest(HelpPageTestCase):
    def test_no_properties(self):
        file = {
            'markdown': 'foo\nbar\n',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state())

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['markdown-properties'], {})

    def test_single_property_no_trailing_nl(self):
        file = {
            'markdown': 'foo\nbar\nbaz:quux',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state())

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['markdown-properties'], {
                'baz': 'quux'
        })

    def test_single_property_trailing_nl(self):
        file = {
            'markdown': 'foo\nbar\nbaz:quux\n',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state())

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['markdown-properties'], {
                'baz': 'quux'
        })

    def test_single_property_blank_before_properties_trailing_nl(self):
        file = {
            'markdown': 'foo\nbar\n\n\nbaz:quux\n',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state())

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['markdown-properties'], {
                'baz': 'quux'
        })

    def test_single_property_blank_before_properties_no_trailing_nl(self):
        file = {
            'markdown': 'foo\nbar\n\n\nbaz:quux',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state())

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['markdown-properties'], {
                'baz': 'quux'
        })

    def test_stripping(self):
        file = {
            'markdown': 'foo\nbar\n  baz  :  quux  ',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state())

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['markdown-properties'], {
                'baz': 'quux'
        })

    def test_alphabet(self):
        file = {
            'markdown': 'foo\nFoo:bar\nba-r:baz\nbar:baz',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state())

        self.assertEqual(file['markdown'], 'foo\nFoo:bar\n')
        self.assertEqual(file['markdown-properties'], {
                'ba-r': 'baz',
                'bar': 'baz',
        })
