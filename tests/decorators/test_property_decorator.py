from tests import DocumentPageTestCase
from document_generator.decorators import PropertyDecorator


class PropertyDecoratorTest(DocumentPageTestCase):
    def test_no_files(self):
        node = {
            'files': {},
            'subnodes': [],
            }

        decorator = PropertyDecorator()
        decorator.run(node, decorator.init_state())

        self.assertEqual(node['files'], {})

    def test_file_and_default(self):
        node = {
            'files': {
                'default': {
                    'key': 'fr',
                    'content-properties': {
                        'only-default': 'default',
                        'default-and-en': 'default',
                        }},
                'en': {
                    'key': 'en',
                    'content-properties': {
                        'only-en': 'en',
                        'default-and-en': 'en',
                        }},
            },
            'subnodes': [],
        }

        decorator = PropertyDecorator()
        decorator.run(node, decorator.init_state())

        self.assertEqual(node['files']['default']['properties'], {
                'language': 'fr',
                'only-default': 'default',
                'default-and-en': 'default',
                })

        self.assertEqual(node['files']['en']['properties'], {
                'language': 'en',
                'only-default': 'default',
                'only-en': 'en',
                'default-and-en': 'en',
                })

    def test_file_default_and_properties(self):
        node = {
            'files': {
                'default': {
                    'key': 'default',
                    'content-properties': {
                        'default-and-en': 'default',
                        'default-and-properties': 'default',
                        'default-and-properties-and-en': 'default',
                        'only-default': 'default',
                        }},
                'en': {
                    'key': 'en',
                    'content-properties': {
                        'default-and-en': 'en',
                        'default-and-properties-and-en': 'en',
                        'en-and-properties': 'en',
                        'only-en': 'en',
                        }},
                'properties': {
                    'key': 'properties',
                    'content-properties': {
                        'default-and-properties': 'properties',
                        'default-and-properties-and-en': 'properties',
                        'en-and-properties': 'properties',
                        'only-properties': 'properties',
                        }},
            },
            'subnodes': [],
        }

        decorator = PropertyDecorator()
        decorator.run(node, decorator.init_state())

        self.assertEqual(node['files']['default']['properties'], {
                        'language': 'default',
                        'default-and-en': 'default',
                        'default-and-properties': 'default',
                        'default-and-properties-and-en': 'default',
                        'en-and-properties': 'properties',
                        'only-default': 'default',
                        'only-properties': 'properties',
                })

        self.assertEqual(node['files']['properties']['properties'], {
                        'language': 'properties',
                        'default-and-en': 'default',
                        'default-and-properties': 'properties',
                        'default-and-properties-and-en': 'properties',
                        'en-and-properties': 'properties',
                        'only-default': 'default',
                        'only-properties': 'properties',
                })

        self.assertEqual(node['files']['en']['properties'], {
                        'language': 'en',
                        'default-and-en': 'en',
                        'default-and-properties': 'properties',
                        'default-and-properties-and-en': 'en',
                        'en-and-properties': 'en',
                        'only-default': 'default',
                        'only-en': 'en',
                        'only-properties': 'properties',
                })

    def test_inheritance(self):
        node11 = {
            'files': {
                'en': {
                    'key': 'en',
                    'content-properties': {
                        'node11-en': 'node11-en',
                        }},
                'default': {
                    'key': 'default',
                    'content-properties': {
                        'node11-default': 'node11-default',
                        'node1-overriden-by-node11': 'node11-default',
                        }},
            },
            'subnodes': [],
        }

        node12 = {
            'files': {
                'en': {
                    'key': 'en',
                    'content-properties': {
                        'node12-en': 'node12-en',
                        }},
                'default': {
                    'key': 'default',
                    'content-properties': {
                        'node12-default': 'node12-default',
                        'node1-overriden-by-node12': 'node12-default',
                        }},
            },
            'subnodes': [],
        }

        node1 = {
            'files': {
                'en': {
                    'key': 'en',
                    'content-properties': {
                        'node1-en': 'node1-en',
                        }},
                'default': {
                    'key': 'default',
                    'content-properties': {
                        'node1-default': 'node1-default',
                        'node1-overriden-by-node11': 'node1-default',
                        'node1-overriden-by-node12': 'node1-default',
                        }},
            },
            'subnodes': [node11, node12],
        }

        decorator = PropertyDecorator()
        decorator.run(node1, decorator.init_state())

        self.assertEqual(node1['files']['en']['properties'], {
                'language': 'en',
                'node1-default': 'node1-default',
                'node1-en': 'node1-en',
                'node1-overriden-by-node11': 'node1-default',
                'node1-overriden-by-node12': 'node1-default',
                })
        self.assertEqual(node1['files']['default']['properties'], {
                'language': 'default',
                'node1-default': 'node1-default',
                'node1-overriden-by-node11': 'node1-default',
                'node1-overriden-by-node12': 'node1-default',
                })

        self.assertEqual(node11['files']['en']['properties'], {
                'language': 'en',
                'node1-default': 'node1-default',
                'node11-default': 'node11-default',
                'node11-en': 'node11-en',
                'node1-overriden-by-node11': 'node11-default',
                'node1-overriden-by-node12': 'node1-default',
                })
        self.assertEqual(node11['files']['default']['properties'], {
                'language': 'default',
                'node1-default': 'node1-default',
                'node11-default': 'node11-default',
                'node1-overriden-by-node11': 'node11-default',
                'node1-overriden-by-node12': 'node1-default',
                })

        self.assertEqual(node12['files']['en']['properties'], {
                'language': 'en',
                'node1-default': 'node1-default',
                'node12-default': 'node12-default',
                'node12-en': 'node12-en',
                'node1-overriden-by-node11': 'node1-default',
                'node1-overriden-by-node12': 'node12-default',
                })
        self.assertEqual(node12['files']['default']['properties'], {
                'language': 'default',
                'node1-default': 'node1-default',
                'node12-default': 'node12-default',
                'node1-overriden-by-node11': 'node1-default',
                'node1-overriden-by-node12': 'node12-default',
                })
