from tests import DocumentPageTestCase
from document_generator.decorators import DefaultFileNodeDecorator


class DefaultFileNodeDecoratorTest(DocumentPageTestCase):
    def test_no_files(self):
        node = {
            'files': {},
            'subnodes': [],
            }

        decorator = DefaultFileNodeDecorator('en')
        decorator.decorate_node(node, decorator.init_state())

        self.assertEqual(node['files'], {})

    def test_single(self):
        node = {
            'files': {
                'en': 'fileEn',
                },
            'subnodes': [],
            }

        decorator = DefaultFileNodeDecorator('en')
        decorator.decorate_node(node, decorator.init_state())

        self.assertEqual(node['files'], {
                'default': 'fileEn',
                'en': 'fileEn',
        })

    def test_multiple(self):
        node = {
            'files': {
                'de': 'fileDe',
                'en': 'fileEn',
                },
            'subnodes': [],
            }

        decorator = DefaultFileNodeDecorator('en')
        decorator.decorate_node(node, decorator.init_state())

        self.assertEqual(node['files'], {
                'de': 'fileDe',
                'default': 'fileEn',
                'en': 'fileEn',
        })

    def test_copy(self):
        node = {
            'files': {
                'de': ['fileDe', 'foo'],
                'en': ['fileEn', 'bar'],
                },
            'subnodes': [],
            }

        decorator = DefaultFileNodeDecorator('en')
        decorator.decorate_node(node, decorator.init_state())

        node['files']['en'].append('baz')

        self.assertEqual(node['files'], {
                'de': ['fileDe', 'foo'],
                'default': ['fileEn', 'bar'],
                'en': ['fileEn', 'bar', 'baz'],
        })
