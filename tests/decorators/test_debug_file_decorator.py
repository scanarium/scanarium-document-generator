from tests import DocumentPageTestCase
from document_generator.decorators import DebugFileDecorator


class DebugFileDecoratorTest(DocumentPageTestCase):
    def decorate(self, file, enabled=True):
        decorator = DebugFileDecorator(enabled)
        decorator.decorate_file(file, decorator.init_state({}))

    def test_empty(self):
        file = {
            'markdown': '',
            'file_name': 'quux',
            }

        self.decorate(file)

        self.assertEqual(file['markdown'], '\n\nquux\n{: class=source-file}\n')

    def test_single_line(self):
        file = {
            'markdown': 'foo',
            'file_name': 'quux',
            }

        self.decorate(file)

        self.assertEqual(file['markdown'],
                         'foo\n\nquux\n{: class=source-file}\n')

    def test_two_lines(self):
        file = {
            'markdown': 'foo\nbar',
            'file_name': 'quux',
            }

        self.decorate(file)

        self.assertEqual(file['markdown'],
                         'foo\n\nquux\n{: class=source-file}\n\nbar')

    def test_plain(self):
        file = {
            'markdown': 'foo\nbar\nbaz',
            'file_name': 'quux',
            }

        self.decorate(file)

        self.assertEqual(file['markdown'],
                         'foo\n\nquux\n{: class=source-file}\n\nbar\nbaz')

    def test_disabled(self):
        file = {
            'markdown': 'foo\nbar\nbaz',
            'file_name': 'quux',
            }

        self.decorate(file, enabled=False)

        self.assertEqual(file['markdown'], 'foo\nbar\nbaz')
