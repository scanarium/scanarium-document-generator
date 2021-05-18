from tests import DocumentPageTestCase
from document_generator.decorators import DefaultFileNodeDecorator


class DefaultFileNodeDecoratorTest(DocumentPageTestCase):
    def decorate(self, node):
        decorator = DefaultFileNodeDecorator('en')
        decorator.decorate_node(node, decorator.init_state(node))

    def test_no_files(self):
        node = {
            'files': {},
            'subnodes': [],
            }

        self.decorate(node)

        self.assertEqual(node['files'], {})

    def test_single(self):
        node = {
            'files': {
                'en': {'name': 'fileEn'},
                },
            'subnodes': [],
            }

        self.decorate(node)

        self.assertEqual(node['files'], {
                'default': {'name': 'fileEn', 'is-default': True},
                'en': {'name': 'fileEn'},
        })

    def test_multiple(self):
        node = {
            'files': {
                'de': {'name': 'fileDe'},
                'en': {'name': 'fileEn'},
                },
            'subnodes': [],
            }

        self.decorate(node)

        self.assertEqual(node['files'], {
                'de': {'name': 'fileDe'},
                'default': {'name': 'fileEn', 'is-default': True},
                'en': {'name': 'fileEn'},
        })

    def test_copy(self):
        node = {
            'files': {
                'de': {'name': 'fileDe'},
                'en': {'name': 'fileEn'},
                },
            'subnodes': [],
            }

        self.decorate(node)

        node['files']['en']['foo'] = 'baz'

        self.assertEqual(node['files'], {
                'de': {'name': 'fileDe'},
                'default': {'name': 'fileEn', 'is-default': True},
                'en': {'name': 'fileEn', 'foo': 'baz'},
        })
