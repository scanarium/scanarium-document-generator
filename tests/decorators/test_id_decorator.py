from tests import DocumentPageTestCase
from document_generator.decorators import IdDecorator


class IdDecoratorTest(DocumentPageTestCase):
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
        self.assertEmpty(messages)

    def test_plain(self):
        node = {
            'name': 'bar',
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
        self.assertEmpty(messages)

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
        self.assertLenIs(messages, 1)

    def test_duplicate_ids(self):
        node11 = {
            'name': 'node11',
            'files': {
                'default': {'properties': {'id': 'id-foo'}},
            },
            'subnodes': [],
        }
        node12 = {
            'name': 'node12',
            'files': {
                'default': {'properties': {'id': 'id-foo'}},
            },
            'subnodes': [],
        }
        node1 = {
            'name': 'node1',
            'files': {
                'default': {'properties': {'id': 'id-node1'}},
                'en': {'properties': {}},
            },
            'subnodes': [node11, node12],
        }

        decorator = IdDecorator()
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertEqual(messages[0]['kind'], 'error')
        self.assertIn('node11', messages[0]['text'])
        self.assertIn('node12', messages[0]['text'])
        self.assertIn('id-foo', messages[0]['text'])
        self.assertLenIs(messages, 1)
