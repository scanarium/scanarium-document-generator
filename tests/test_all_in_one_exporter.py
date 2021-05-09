import os
import tempfile

from .environment import HelpPageTestCase
from help_generator import AllInOneExporter

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'help-node-parser')


class AllInOneExporterTest(HelpPageTestCase):
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
        with tempfile.TemporaryDirectory(prefix='help-generator-test-') as dir:
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
