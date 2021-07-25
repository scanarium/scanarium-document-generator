from tests import DocumentPageTestCase
from document_generator.decorators import VersionCheckDecorator

MAJOR_VERSION_MISMATCH_NODE = {
    'files': {
        'en': {
            'key': 'en',
            'properties': {
                'version': '11.003',
                }},
        'default': {
            'key': 'de',
            'properties': {
                'version': '1.003',
                }},
        },
    'subnodes': [],
    }


class VersionCheckDecoratorTest(DocumentPageTestCase):
    def run_decorator(self, node, actions=None):
        if actions is None:
            decorator = VersionCheckDecorator()
        else:
            decorator = VersionCheckDecorator(actions=actions)
        state = decorator.init_state(node)
        decorator.run(node, state)
        return decorator.get_messages(state)

    def test_no_files(self):
        node = {
            'files': {},
            'subnodes': [],
            }

        messages = self.run_decorator(node)
        self.assertEmpty(messages)

    def test_full_match(self):
        node = {
            'files': {
                'en': {
                    'key': 'en',
                    'properties': {
                        'version': '1.003',
                        }},
                'default': {
                    'key': 'de',
                    'properties': {
                        'version': '1.003',
                        }},
            },
            'subnodes': [],
        }

        messages = self.run_decorator(node)
        self.assertEmpty(messages)

    def test_mismatch_minor(self):
        node = {
            'files': {
                'en': {
                    'key': 'en',
                    'properties': {
                        'version': '1.004',
                        }},
                'default': {
                    'key': 'de',
                    'properties': {
                        'version': '1.003',
                        }},
            },
            'subnodes': [],
        }

        messages = self.run_decorator(node)
        self.assertEmpty(messages)

    def test_mismatch_major_default(self):
        messages = self.run_decorator(MAJOR_VERSION_MISMATCH_NODE)
        self.assertLenIs(messages, 1)
        self.assertIn('ismatch', str(messages[0]['text']))
        self.assertEqual('error', messages[0]['kind'])

    def test_mismatch_major_action_error(self):
        messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['error'])
        self.assertLenIs(messages, 1)
        self.assertIn('ismatch', str(messages[0]['text']))
        self.assertEqual('error', messages[0]['kind'])

    def test_mismatch_major_action_ignore(self):
        messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['ignore'])
        self.assertLenIs(messages, 0)

    def test_mismatch_major_action_warn(self):
        messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['warning'])
        self.assertLenIs(messages, 1)
        self.assertIn('ismatch', str(messages[0]['text']))
        self.assertEqual('warning', messages[0]['kind'])

    def test_mismatch_major_action_multiple(self):
        messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['error', 'warning'])
        self.assertLenIs(messages, 2)
        self.assertIn('ismatch', str(messages[0]['text']))
        self.assertEqual('error', messages[0]['kind'])
        self.assertIn('ismatch', str(messages[1]['text']))
        self.assertEqual('warning', messages[1]['kind'])

    def test_mismatch_major_action_unknown(self):
        messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['foo'])
        self.assertLenIs(messages, 1)
        self.assertIn('"foo"', str(messages[0]['text']))
        self.assertEqual('error', messages[0]['kind'])

    def test_subnode(self):
        node11 = {
            'files': {
                'en': {
                    'key': 'en',
                    'properties': {
                        'version': '11.003',
                        }},
                'default': {
                    'key': 'de',
                    'properties': {
                        'version': '11.003',
                        }},
            },
            'subnodes': [],
        }

        node12 = {
            'files': {
                'en': {
                    'key': 'en',
                    'properties': {
                        'version': '12.003',
                        }},
                'default': {
                    'key': 'de',
                    'properties': {
                        'version': '12.003',
                        }},
            },
            'subnodes': [],
        }

        node = {
            'files': {
                'en': {
                    'key': 'en',
                    'properties': {
                        'version': '1.003',
                        }},
                'default': {
                    'key': 'de',
                    'properties': {
                        'version': '1.003',
                        }},
            },
            'subnodes': [node11, node12],
        }

        messages = self.run_decorator(node)
        self.assertEmpty(messages)
