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
            self.assertIn('<html', contents)
            self.assertIn('fooEn', contents)
            self.assertIn('barEn', contents)

            with open(os.path.join(dir, 'all.html.de')) as f:
                contents = f.read()
            self.assertIn('<html', contents)
            self.assertIn('fooDe', contents)
            self.assertIn('barEn', contents)
