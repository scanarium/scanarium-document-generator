import os

from .environment import DocumentPageTestCase
from document_generator import AllInOneExporter

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
                    'markdown': 'barEn'
                    },
                'eo': {
                    'markdown': 'barEo'
                    },
            },
            'subnodes': [node11],
        }
        with self.tempDir() as dir:
            exporter = AllInOneExporter(node1, dir, 'en', ['de'])
            exporter.export()

            with open(os.path.join(dir, 'all.html.en')) as f:
                contents = f.read()
            self.assertStartsWith(contents, '<html')
            self.assertIn('fooEn', contents)
            self.assertIn('barEn', contents)
            self.assertEndsWith(contents, '</html>')

            with open(os.path.join(dir, 'all.html.de')) as f:
                contents = f.read()
            self.assertStartsWith(contents, '<html')
            self.assertIn('fooDe', contents)
            self.assertIn('barEn', contents)
            self.assertEndsWith(contents, '</html>')

    def test_template_header(self):
        node1 = {
            'files': {
                'en': {
                    'markdown': 'fooEn'
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

            with open(os.path.join(dir, 'all.html.en')) as f:
                contents = f.read()

            self.assertStartsWith(contents, 'HEADER')
            self.assertIn('fooEn', contents)
            self.assertEndsWith(contents, '</html>')

    def test_template_footer(self):
        node1 = {
            'files': {
                'en': {
                    'markdown': 'fooEn'
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

            with open(os.path.join(dir, 'all.html.en')) as f:
                contents = f.read()

            self.assertStartsWith(contents, '<html')
            self.assertIn('fooEn', contents)
            self.assertEndsWith(contents, 'FOOTER')
