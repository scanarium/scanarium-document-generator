from tests import DocumentPageTestCase
from document_generator.decorators import IdDecorator


class DefaultFileNodeDecoratorTest(DocumentPageTestCase):
    def test_no_files(self):
        node = {
            'files': {},
            'subnodes': [],
            }

        decorator = IdDecorator()
        decorator.run(node, decorator.init_state())

        self.assertEqual(node['files'], {})

    def test_plain(self):
        node = {
            'files': {
                'default': {'properties': {'id': 'id-foo'}},
                'en': {'properties': {}},
            },
            'subnodes': [],
        }

        decorator = IdDecorator()
        decorator.run(node, decorator.init_state())

        self.assertEqual(node['files'], {
                'default': {
                    'id': 'id-foo',
                    'properties': {'id': 'id-foo'}
                },
                'en': {'id': 'id-foo', 'properties': {}},
                })
