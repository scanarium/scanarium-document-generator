from tests import DocumentPageTestCase
from document_generator.decorators import LevelDecorator


class LevelDecoratorTest(DocumentPageTestCase):
    def test_no_files(self):
        node = {
            'files': {},
            'subnodes': [],
            }

        decorator = LevelDecorator()
        decorator.run(node, decorator.init_state())

        self.assertEqual(node['files'], {})

    def test_single_file(self):
        node = {
            'files': {'en': {}},
            'subnodes': [],
            }

        decorator = LevelDecorator()
        decorator.run(node, decorator.init_state())

        self.assertEqual(node['files'], {'en': {'level': 1}})

    def test_multiple_file(self):
        node = {
            'files': {'en': {}, 'de': {}},
            'subnodes': [],
            }

        decorator = LevelDecorator()
        decorator.run(node, decorator.init_state())

        self.assertEqual(node['files'], {
                'en': {'level': 1},
                'de': {'level': 1},
                })

    def test_subnodes(self):
        node = {
            'files': {'en': {}},
            'subnodes': [
                {
                    'files': {'de': {}},
                    'subnodes': [],
                },
                ]
            }

        decorator = LevelDecorator()
        decorator.run(node, decorator.init_state())

        self.assertEqual(node['files'], {
                'en': {'level': 1},
                })

        self.assertEqual(node['subnodes'][0]['files'], {
                'de': {'level': 2},
                })
