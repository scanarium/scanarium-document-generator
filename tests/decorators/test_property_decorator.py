from tests import DocumentPageTestCase
from document_generator.decorators import PropertyDecorator


class PropertyDecoratorTest(DocumentPageTestCase):
    def run_decorator(self, node):
        decorator = PropertyDecorator(initial_state={
                'global': 'global',
                'global-maybe-overridden': 'global',
                })
        decorator.run(node, decorator.init_state(node))

    def test_no_files(self):
        node = {
            'files': {},
            'subnodes': [],
            }

        self.run_decorator(node)

        self.assertEqual(node['files'], {})

    def test_file(self):
        node = {
            'files': {
                'en': {
                    'key': 'en',
                    'content-properties': {
                        'global-maybe-overridden': 'en',
                        'only-en': 'en',
                        }},
            },
            'subnodes': [],
        }

        self.run_decorator(node)

        self.assertEqual(node['files']['en']['properties'], {
                'global': 'global',
                'global-maybe-overridden': 'en',
                'language': 'en',
                'only-en': 'en',
                })

    def test_file_with_properties_file(self):
        node = {
            'files': {
                'en': {
                    'key': 'en',
                    'content-properties': {
                        'en-and-properties': 'en',
                        'only-en': 'en',
                        }},
                'properties': {
                    'key': 'properties',
                    'content-properties': {
                        'en-and-properties': 'properties',
                        'global-maybe-overridden': 'properties',
                        'only-properties': 'properties',
                        }},
            },
            'subnodes': [],
        }

        self.run_decorator(node)

        self.assertEqual(node['files']['en']['properties'], {
                'en-and-properties': 'en',
                'global': 'global',
                'global-maybe-overridden': 'properties',
                'language': 'en',
                'only-en': 'en',
                'only-properties': 'properties',
                })

    def test_tree_without_default_parent(self):
        node1 = {
            'files': {
                'en': {
                    'key': 'en',
                    'content-properties': {
                        'en-and-properties': 'en',
                        'only-en': 'en',
                        'only-lang': 'en',
                        }},
                'de': {
                    'key': 'de',
                    'content-properties': {
                        'de-and-properties': 'de',
                        'only-de': 'de',
                        'only-lang': 'de',
                        }},
                'properties': {
                    'key': 'properties',
                    'content-properties': {
                        'en-and-properties': 'properties',
                        'only-properties': 'properties',
                        }},
            },
            'subnodes': [],
        }

        node = {
            'files': {
                'en': {
                    'key': 'en',
                    'content-properties': {
                        'global-maybe-overridden': 'en',
                        }},
                'properties': {
                    'key': 'properties',
                    'content-properties': {
                        'global-maybe-overridden': 'properties',
                        }},
            },
            'subnodes': [node1],
        }

        self.run_decorator(node)

        self.assertEqual(node['files']['en']['properties'], {
                'global': 'global',
                'global-maybe-overridden': 'en',
                'language': 'en',
                })

        self.assertEqual(node1['files']['en']['properties'], {
                'en-and-properties': 'en',
                'global': 'global',
                'global-maybe-overridden': 'en',
                'language': 'en',
                'only-en': 'en',
                'only-lang': 'en',
                'only-properties': 'properties',
                })

        self.assertEqual(node1['files']['de']['properties'], {
                'de-and-properties': 'de',
                'en-and-properties': 'properties',
                'global': 'global',
                'global-maybe-overridden': 'properties',
                'language': 'de',
                'only-de': 'de',
                'only-lang': 'de',
                'only-properties': 'properties',
                })

    def test_tree_with_default_parent(self):
        node1 = {
            'files': {
                'en': {
                    'key': 'en',
                    'content-properties': {
                        'en-and-properties': 'en',
                        'only-en': 'en',
                        'only-lang': 'en',
                        }},
                'de': {
                    'key': 'de',
                    'content-properties': {
                        'de-and-properties': 'de',
                        'only-de': 'de',
                        'only-lang': 'de',
                        }},
                'properties': {
                    'key': 'properties',
                    'content-properties': {
                        'en-and-properties': 'properties',
                        'only-properties': 'properties',
                        }},
            },
            'subnodes': [],
        }

        node = {
            'files': {
                'default': {
                    'key': 'en',
                    'is-default': True,
                    'content-properties': {
                        'global-maybe-overridden': 'en',
                        'only-default': 'default',
                        }},
                'properties': {
                    'key': 'properties',
                    'content-properties': {
                        'global-maybe-overridden': 'properties',
                        }},
            },
            'subnodes': [node1],
        }

        self.run_decorator(node)

        self.assertEqual(node['files']['default']['properties'], {
                'global': 'global',
                'global-maybe-overridden': 'en',
                'language': 'en',
                'only-default': 'default',
                })

        self.assertEqual(node1['files']['en']['properties'], {
                'en-and-properties': 'en',
                'global': 'global',
                'global-maybe-overridden': 'en',
                'language': 'en',
                'only-default': 'default',
                'only-en': 'en',
                'only-lang': 'en',
                'only-properties': 'properties',
                })

        self.assertEqual(node1['files']['de']['properties'], {
                'de-and-properties': 'de',
                'en-and-properties': 'properties',
                'global': 'global',
                'global-maybe-overridden': 'en',
                'language': 'de',
                'only-de': 'de',
                'only-default': 'default',
                'only-lang': 'de',
                'only-properties': 'properties',
                })
