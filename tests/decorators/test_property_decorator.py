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
                'default': {'content-properties': {
                        'only-default': 'default',
                        'default-and-en': 'default',
                        }},
                'en': {'content-properties': {
                        'only-en': 'en',
                        'default-and-en': 'en',
                        }},
            },
            'subnodes': [],
        }

        decorator = PropertyDecorator()
        decorator.run(node, decorator.init_state())

        self.assertEqual(node['files']['default']['properties'], {
                'only-default': 'default',
                'default-and-en': 'default',
                })

        self.assertEqual(node['files']['en']['properties'], {
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
                        'default-and-en': 'default',
                        'default-and-properties': 'default',
                        'default-and-properties-and-en': 'default',
                        'en-and-properties': 'properties',
                        'only-default': 'default',
                        'only-properties': 'properties',
                })

        self.assertEqual(node['files']['properties']['properties'], {
                        'default-and-en': 'default',
                        'default-and-properties': 'properties',
                        'default-and-properties-and-en': 'properties',
                        'en-and-properties': 'properties',
                        'only-default': 'default',
                        'only-properties': 'properties',
                })

        self.assertEqual(node['files']['en']['properties'], {
                        'default-and-en': 'en',
                        'default-and-properties': 'properties',
                        'default-and-properties-and-en': 'en',
                        'en-and-properties': 'en',
                        'only-default': 'default',
                        'only-en': 'en',
                        'only-properties': 'properties',
                })
