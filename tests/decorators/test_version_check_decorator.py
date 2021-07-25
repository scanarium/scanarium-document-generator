import copy


from tests import DocumentPageTestCase
from document_generator.decorators import VersionCheckDecorator

MAJOR_VERSION_MISMATCH_NODE = {
    'files': {
        'en': {
            'key': 'en',
            'properties': {
                'version': '11.003',
                },
            'markdown': 'fileEn',
            },
        'default': {
            'key': 'de',
            'properties': {
                'version': '2.003',
                },
            'markdown': 'fileDefault',
            },
        },
    'subnodes': [],
    }


class VersionCheckDecoratorTest(DocumentPageTestCase):
    def run_decorator(self, node, actions=None):
        if actions is None:
            decorator = VersionCheckDecorator()
        else:
            decorator = VersionCheckDecorator(actions=actions)
        node = copy.deepcopy(node)
        state = decorator.init_state(node)
        decorator.run(node, state)
        return node, decorator.get_messages(state)

    def test_no_files(self):
        node = {
            'files': {},
            'subnodes': [],
            }

        _, messages = self.run_decorator(node)
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

        _, messages = self.run_decorator(node)
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

        _, messages = self.run_decorator(node)
        self.assertEmpty(messages)

    def test_mismatch_major_default(self):
        node, messages = self.run_decorator(MAJOR_VERSION_MISMATCH_NODE)
        self.assertLenIs(messages, 1)
        self.assertIn('ismatch', str(messages[0]['text']))
        self.assertEqual('error', messages[0]['kind'])

        self.assertStartsWith(node['files']['en']['markdown'], 'fileEn')
        self.assertStartsWith(node['files']['default']['markdown'], 'fileDef')

    def test_mismatch_major_action_error(self):
        node, messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['error'])
        self.assertLenIs(messages, 1)
        self.assertIn('ismatch', str(messages[0]['text']))
        self.assertEqual('error', messages[0]['kind'])

        self.assertStartsWith(node['files']['en']['markdown'], 'fileEn')
        self.assertStartsWith(node['files']['default']['markdown'], 'fileDef')

    def test_mismatch_major_action_ignore(self):
        node, messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['ignore'])
        self.assertLenIs(messages, 0)

        self.assertStartsWith(node['files']['en']['markdown'], 'fileEn')
        self.assertStartsWith(node['files']['default']['markdown'], 'fileDef')

    def test_mismatch_major_action_warn(self):
        node, messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['warning'])
        self.assertLenIs(messages, 1)
        self.assertIn('ismatch', str(messages[0]['text']))
        self.assertEqual('warning', messages[0]['kind'])

        self.assertStartsWith(node['files']['en']['markdown'], 'fileEn')
        self.assertStartsWith(node['files']['default']['markdown'], 'fileDef')

    def test_mismatch_major_action_append_macro(self):
        node, messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['append-macro-foo'])
        self.assertEmpty(messages)

        markdown = node['files']['en']['markdown']
        self.assertStartsWith(markdown, 'fileEn\n{=macro(foo, ')
        self.assertIn('11.003', markdown)
        self.assertIn('2.003', markdown)

        self.assertStartsWith(node['files']['default']['markdown'], 'fileDef')

    def test_mismatch_major_action_multiple(self):
        node, messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['error', 'warning'])
        self.assertLenIs(messages, 2)
        self.assertIn('ismatch', str(messages[0]['text']))
        self.assertEqual('error', messages[0]['kind'])
        self.assertIn('ismatch', str(messages[1]['text']))
        self.assertEqual('warning', messages[1]['kind'])

        self.assertStartsWith(node['files']['en']['markdown'], 'fileEn')
        self.assertStartsWith(node['files']['default']['markdown'], 'fileDef')

    def test_mismatch_major_action_unknown(self):
        node, messages = self.run_decorator(
            MAJOR_VERSION_MISMATCH_NODE, actions=['foo'])
        self.assertLenIs(messages, 1)
        self.assertIn('"foo"', str(messages[0]['text']))
        self.assertEqual('error', messages[0]['kind'])

        self.assertStartsWith(node['files']['en']['markdown'], 'fileEn')
        self.assertStartsWith(node['files']['default']['markdown'], 'fileDef')

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

        _, messages = self.run_decorator(node)
        self.assertEmpty(messages)
