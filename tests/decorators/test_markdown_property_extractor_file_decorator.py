from tests import DocumentPageTestCase
from document_generator.decorators import \
    MarkdownPropertyExtractorFileDecorator


class MarkdownPropertyExtractorFileDecoratorTest(DocumentPageTestCase):
    def test_no_properties(self):
        file = {
            'raw-content': 'foo\nbar\n',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['content-properties'], {})

    def test_single_property_no_trailing_nl(self):
        file = {
            'raw-content': 'foo\nbar\nbaz:quux',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['content-properties'], {
                'baz': 'quux'
        })

    def test_single_property_trailing_nl(self):
        file = {
            'raw-content': 'foo\nbar\nbaz:quux\n',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['content-properties'], {
                'baz': 'quux'
        })

    def test_single_property_blank_before_properties_trailing_nl(self):
        file = {
            'raw-content': 'foo\nbar\n\n\nbaz:quux\n',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['content-properties'], {
                'baz': 'quux'
        })

    def test_single_property_blank_before_properties_no_trailing_nl(self):
        file = {
            'raw-content': 'foo\nbar\n\n\nbaz:quux',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['content-properties'], {
                'baz': 'quux'
        })

    def test_stripping(self):
        file = {
            'raw-content': 'foo\nbar\n  baz  :  quux  ',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], 'foo\nbar\n')
        self.assertEqual(file['content-properties'], {
                'baz': 'quux'
        })

    def test_alphabet(self):
        file = {
            'raw-content': 'foo\nFoo:bar\nba-r:baz\nbar:baz',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], 'foo\nFoo:bar\n')
        self.assertEqual(file['content-properties'], {
                'ba-r': 'baz',
                'bar': 'baz',
        })

    def test_multiple(self):
        file = {
            'raw-content': 'foo\nfoo:bar\nbar:baz',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], 'foo\n')
        self.assertEqual(file['content-properties'], {
                'foo': 'bar',
                'bar': 'baz',
        })

    def test_multiple_empty_line(self):
        file = {
            'raw-content': 'foo\nfoo:bar\n\nbar:baz',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], 'foo\n')
        self.assertEqual(file['content-properties'], {
                'foo': 'bar',
                'bar': 'baz',
        })

    def test_multiple_whitespace_line(self):
        file = {
            'raw-content': 'foo\nfoo:bar\n \nbar:baz',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], 'foo\n')
        self.assertEqual(file['content-properties'], {
                'foo': 'bar',
                'bar': 'baz',
        })

    def test_only_properties_with_whitespace_line(self):
        file = {
            'raw-content': '\nfoo:bar\n\n',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], '')
        self.assertEqual(file['content-properties'], {'foo': 'bar'})

    def test_only_properties_without_whitespace_line(self):
        file = {
            'raw-content': 'foo:bar',
            }
        decorator = MarkdownPropertyExtractorFileDecorator()

        decorator.decorate_file(file, decorator.init_state({}))

        self.assertEqual(file['markdown'], '')
        self.assertEqual(file['content-properties'], {'foo': 'bar'})
