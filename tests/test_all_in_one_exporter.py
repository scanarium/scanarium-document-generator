import os

from .environment import DocumentPageTestCase
from document_generator import AllInOneExporter
from document_generator.decorators import ValueInjectorFileDecorator

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'document-node-parser')


class AllInOneExporterTest(DocumentPageTestCase):
    def test_simple(self):
        node111 = {
            'files': {
                'en': {
                    'markdown': 'fooEn',
                    },
                'de': {
                    'markdown': 'fooDe',
                    },
                'fr': {
                    'markdown': 'fooFr',
                    },
            },
            'subnodes': [],
        }
        node11 = {
            'files': {},
            'subnodes': [node111],
        }
        node1 = {
            'files': {
                'en': {
                    'markdown': 'barEn',
                    'properties': {},
                    },
                'eo': {
                    'markdown': 'barEo',
                    'properties': {},
                    },
                'default': {
                    'markdown': 'barDefault',
                    'properties': {},
                    },
            },
            'subnodes': [node11],
        }
        with self.tempDir() as dir:
            exporter = AllInOneExporter(node1, dir, 'en', ['de'])
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.html.en'))
            self.assertStartsWith(contents, '<html')
            self.assertIn('fooEn', contents)
            self.assertIn('barEn', contents)
            self.assertEndsWith(contents, '</html>')

            contents = self.get_file_contents(os.path.join(dir, 'all.html.de'))
            self.assertStartsWith(contents, '<html')
            self.assertIn('fooDe', contents)
            self.assertIn('barEn', contents)
            self.assertEndsWith(contents, '</html>')

            contents = self.get_file_contents(os.path.join(dir, 'all.md.en'))
            self.assertStartsWith(contents, 'barEn')
            self.assertEndsWith(contents, 'fooEn')

            contents = self.get_file_contents(os.path.join(dir, 'all.md.de'))
            self.assertStartsWith(contents, 'barEn')
            self.assertEndsWith(contents, 'fooDe')

    def test_template_header(self):
        node1 = {
            'files': {
                'en': {
                    'markdown': 'fooEn',
                    'properties': {},
                    },
                'default': {
                    'markdown': '',
                    'properties': {},
                    },
                },
            'subnodes': [],
            }

        with self.tempDir() as dir:
            template = 'HEADER'
            template_file = os.path.join(dir, 'template-header')
            with open(template_file, 'w+') as f:
                f.write(template)

            conf = {
                'html-header-file': template_file,
                }

            exporter = AllInOneExporter(node1, dir, 'en', [], conf)
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.html.en'))

            self.assertStartsWith(contents, 'HEADER')
            self.assertIn('fooEn', contents)
            self.assertEndsWith(contents, '</html>')

            self.assertFileContents(os.path.join(dir, 'all.md.en'), 'fooEn')

    def test_template_footer(self):
        node1 = {
            'files': {
                'en': {
                    'markdown': 'fooEn',
                    'properties': {},
                    },
                'default': {
                    'markdown': '',
                    'properties': {},
                    },
                },
            'subnodes': [],
            }

        with self.tempDir() as dir:
            template = 'FOOTER'
            template_file = os.path.join(dir, 'template-footer')
            with open(template_file, 'w+') as f:
                f.write(template)

            conf = {
                'html-footer-file': template_file,
                }

            exporter = AllInOneExporter(node1, dir, 'en', [], conf)
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.html.en'))

            self.assertStartsWith(contents, '<html')
            self.assertIn('fooEn', contents)
            self.assertEndsWith(contents, 'FOOTER')

            self.assertFileContents(os.path.join(dir, 'all.md.en'), 'fooEn')

    def test_template_file(self):
        node1 = {
            'files': {
                'en': {
                    'markdown': 'fooEn',
                    'properties': {},
                    },
                'default': {
                    'markdown': 'fooEn',
                    'properties': {},
                    },
                },
            'subnodes': [],
            }

        with self.tempDir() as dir:
            template = '\n'.join([
                    'HEADER1',
                    'HEADER2',
                    '<!-- HEADER-END -->',
                    'OMITTED1',
                    'OMITTED2',
                    '<!-- FOOTER-START -->',
                    'FOOTER1',
                    'FOOTER2',
                    ])
            template_file = os.path.join(dir, 'template')
            with open(template_file, 'w+') as f:
                f.write(template)

            conf = {
                'html-template-file': template_file,
                }

            exporter = AllInOneExporter(node1, dir, 'en', [], conf)
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.html.en'))

            self.assertStartsWith(contents, 'HEADER1')
            self.assertIn('HEADER2', contents)
            self.assertIn('fooEn', contents)
            self.assertIn('FOOTER1', contents)
            self.assertEndsWith(contents, 'FOOTER2')

            self.assertNotIn('OMITTED', contents)

            self.assertFileContents(os.path.join(dir, 'all.md.en'), 'fooEn')

    def test_properties(self):
        node1 = {
            'files': {
                'en': {
                    'markdown': 'fooEn',
                    'properties': {
                        'foo': 'bar',
                        },
                    },
                'default': {
                    'markdown': '',
                    'properties': {},
                    },
                },
            'subnodes': [],
            }

        with self.tempDir() as dir:
            template = '\n'.join([
                    'HEADER1{=property(foo)}',
                    'HEADER2',
                    '<!-- HEADER-END -->',
                    'OMITTED1',
                    'OMITTED2',
                    '<!-- FOOTER-START -->',
                    'FOOTER1{=property(foo)}',
                    'FOOTER2',
                    ])
            template_file = os.path.join(dir, 'template')
            with open(template_file, 'w+') as f:
                f.write(template)

            conf = {
                'html-template-file': template_file,
                }

            value_injector = ValueInjectorFileDecorator()
            value_injector_state = value_injector.init_state(node1)
            exporter = AllInOneExporter(
                node1, dir, 'en', [], conf, value_injector=value_injector,
                value_injector_state=value_injector_state)
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.html.en'))

            self.assertStartsWith(contents, 'HEADER1bar')
            self.assertIn('HEADER2', contents)
            self.assertIn('fooEn', contents)
            self.assertIn('FOOTER1bar', contents)
            self.assertEndsWith(contents, 'FOOTER2')

            self.assertNotIn('OMITTED', contents)

            self.assertFileContents(os.path.join(dir, 'all.md.en'), 'fooEn')
