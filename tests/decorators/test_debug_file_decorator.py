from tests import DocumentPageTestCase
from document_generator.decorators import DebugFileDecorator


class DebugFileDecoratorTest(DocumentPageTestCase):
    def decorate(self, file, enabled=True):
        decorator = DebugFileDecorator(enabled)
        decorator.decorate_file(file, decorator.init_state({}))

    def test_empty(self):
        file = {
            'markdown': '',
            'id': 'foo',
            'file_name': 'quux',
            }

        self.decorate(file)

        expected = '\n'
        expected += '\nid: foo\n{: class=debug-node-id}\n'
        expected += '\nquux\n{: class=debug-source-file}\n'
        self.assertEqual(file['markdown'], expected)

    def test_single_line(self):
        file = {
            'markdown': 'foo',
            'id': 'bar',
            'file_name': 'quux',
            }

        self.decorate(file)

        expected = 'foo\n'
        expected += '\nid: bar\n{: class=debug-node-id}\n'
        expected += '\nquux\n{: class=debug-source-file}\n'
        self.assertEqual(file['markdown'], expected)

    def test_two_lines(self):
        file = {
            'markdown': 'foo\nbar',
            'id': 'baz',
            'file_name': 'quux',
            }

        self.decorate(file)

        expected = 'foo\n'
        expected += '\nid: baz\n{: class=debug-node-id}\n'
        expected += '\nquux\n{: class=debug-source-file}\n'
        expected += '\nbar'
        self.assertEqual(file['markdown'], expected)

    def test_plain(self):
        file = {
            'markdown': 'foo\nbar\nbaz',
            'id': 'quuux',
            'file_name': 'quux',
            }

        self.decorate(file)

        expected = 'foo\n'
        expected += '\nid: quuux\n{: class=debug-node-id}\n'
        expected += '\nquux\n{: class=debug-source-file}\n'
        expected += '\nbar\nbaz'
        self.assertEqual(file['markdown'], expected)

    def test_disabled(self):
        file = {
            'markdown': 'foo\nbar\nbaz',
            'id': 'quuux',
            'file_name': 'quux',
            }

        self.decorate(file, enabled=False)

        self.assertEqual(file['markdown'], 'foo\nbar\nbaz')
