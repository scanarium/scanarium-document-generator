from tests import DocumentPageTestCase
from document_generator.decorators import IdTitleCollectorFileDecorator


class IdTitleCollectorFileDecoratorTest(DocumentPageTestCase):
    def decorate(self, node):
        decorator = IdTitleCollectorFileDecorator()
        state = decorator.init_state(node)
        decorator.run(node, state)
        return (state, decorator)

    def test_no_files(self):
        node = {
            'files': {},
            'subnodes': [],
            }

        state, decorator = self.decorate(node)

        self.assertEmpty(state['id-title-map'])

        self.assertEmpty(decorator.get_messages(state))

    def test_plain(self):
        node = {
            'name': 'bar',
            'files': {
                'en': {
                    'id': 'id-foo',
                    'key': 'en',
                    'markdown': 'foo\nbar',
                },
            },
            'subnodes': [],
        }

        state, decorator = self.decorate(node)

        self.assertEqual(state['id-title-map']['id-foo']['en'], 'foo')
        self.assertLenIs(state['id-title-map']['id-foo'], 1)

        self.assertEmpty(decorator.get_messages(state))

    def test_multiple_files(self):
        node = {
            'name': 'bar',
            'files': {
                'en': {
                    'id': 'id-foo',
                    'key': 'en',
                    'markdown': 'foo\nbar',
                },
                'de': {
                    'id': 'id-foo',
                    'key': 'de',
                    'markdown': 'quux\nbar',
                },
            },
            'subnodes': [],
        }

        state, decorator = self.decorate(node)

        self.assertEqual(state['id-title-map']['id-foo']['en'], 'foo')
        self.assertEqual(state['id-title-map']['id-foo']['de'], 'quux')
        self.assertLenIs(state['id-title-map']['id-foo'], 2)

        self.assertEmpty(decorator.get_messages(state))

    def test_empty_lines(self):
        node = {
            'name': 'bar',
            'files': {
                'en': {
                    'id': 'id-foo',
                    'key': 'en',
                    'markdown': '\n  \nfoo\nbar',
                },
            },
            'subnodes': [],
        }

        state, decorator = self.decorate(node)

        self.assertEqual(state['id-title-map']['id-foo']['en'], 'foo')
        self.assertLenIs(state['id-title-map']['id-foo'], 1)

        self.assertEmpty(decorator.get_messages(state))

    def test_section_marker_stripping(self):
        node = {
            'name': 'bar',
            'files': {
                'en': {
                    'id': 'id-foo',
                    'key': 'en',
                    'markdown': '## # # foo\nbar',
                },
            },
            'subnodes': [],
        }

        state, decorator = self.decorate(node)

        self.assertEqual(state['id-title-map']['id-foo'],
                         {'en': 'foo'})

        self.assertEmpty(decorator.get_messages(state))

    def test_attribute_stripping(self):
        node = {
            'name': 'bar',
            'files': {
                'en': {
                    'id': 'id-foo',
                    'key': 'en',
                    'markdown': 'foo {=BAR} {: class=quux}\nbar',
                },
            },
            'subnodes': [],
        }

        state, decorator = self.decorate(node)

        self.assertEqual(state['id-title-map']['id-foo'],
                         {'en': 'foo {=BAR}'})

        self.assertEmpty(decorator.get_messages(state))

    def test_anonymous(self):
        node = {
            'name': 'bar',
            'files': {
                'en': {
                    'id': 'id-foo',
                    'key': 'en',
                    'markdown': '',
                },
            },
            'subnodes': [],
        }

        state, decorator = self.decorate(node)

        self.assertEqual(state['id-title-map']['id-foo'],
                         {'en': '(anonymous)'})

        messages = decorator.get_messages(state)
        self.assertEqual(messages[0]['kind'], 'error')
        self.assertIn('title', messages[0]['text'])
        self.assertLenIs(messages, 1)

    def test_default(self):
        node = {
            'name': 'bar',
            'files': {
                'default': {
                    'id': 'id-foo',
                    'key': 'en',
                    'is-default': True,
                    'markdown': 'foo'
                },
            },
            'subnodes': [],
        }

        state, decorator = self.decorate(node)

        self.assertEqual(state['id-title-map']['id-foo'],
                         {'default': 'foo'})

        self.assertEmpty(decorator.get_messages(state))
