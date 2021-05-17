from tests import DocumentPageTestCase
from document_generator.decorators import IdDecorator


class DefaultFileNodeDecoratorTest(DocumentPageTestCase):
    def test_no_files(self):
        node = {
            'files': {},
            'subnodes': [],
            }

        decorator = IdDecorator()
        state = decorator.init_state()
        decorator.run(node, state)

        self.assertEqual(node['files'], {})

        messages = decorator.get_messages(state)
        self.assertEqual(len(messages), 0)

    def test_plain(self):
        node = {
            'files': {
                'default': {'properties': {'id': 'id-foo'}},
                'en': {'properties': {}},
            },
            'subnodes': [],
        }

        decorator = IdDecorator()
        state = decorator.init_state()
        decorator.run(node, state)

        self.assertEqual(node['files'], {
                'default': {
                    'id': 'id-foo',
                    'properties': {'id': 'id-foo'}
                },
                'en': {'id': 'id-foo', 'properties': {}},
                })

        messages = decorator.get_messages(state)
        self.assertEqual(len(messages), 0)

    def test_missing_id(self):
        node = {
            'name': 'foo',
            'files': {
                'default': {'properties': {'foo': 'bar'}},
                'en': {'properties': {}},
            },
            'subnodes': [],
        }

        decorator = IdDecorator()
        state = decorator.init_state()
        decorator.run(node, state)

        self.assertEqual(node['files'], {
                'default': {'id': 'anonymous', 'properties': {'foo': 'bar'}},
                'en': {'id': 'anonymous', 'properties': {}},
                })

        messages = decorator.get_messages(state)
        self.assertIn('missing', messages[0]['text'])
        self.assertEqual(messages[0]['kind'], 'error')
        self.assertEqual(len(messages), 1)
