from tests import DocumentPageTestCase
from document_generator.decorators import VersionCheckDecorator


class VersionCheckDecoratorTest(DocumentPageTestCase):
    def run_decorator(self, node):
        decorator = VersionCheckDecorator()
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

    def test_mismatch_major(self):
        node = {
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

        messages = self.run_decorator(node)
        self.assertLenIs(messages, 1)
        self.assertIn('ismatch', messages[0]['text'])

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
