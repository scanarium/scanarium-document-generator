import os
import tempfile

from .environment import HelpPageTestCase
from help_generator import HelpGenerator

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'help-node-parser')


class HelpGeneratorTest(HelpPageTestCase):
    def test_simple(self):
        with tempfile.TemporaryDirectory(prefix='help-generator-test-') as dir:
            fixture_dir = os.path.join(FIXTURE_DIR, 'simple')
            generator = HelpGenerator()
            generator.run({
                    'source': fixture_dir,
                    'target': dir,
                    'default_l10n': 'en',
                    'additional_l10ns': ['de'],
                    })

            with open(os.path.join(dir, 'all.html.en')) as f:
                contents = f.read()
            self.assertIn('<html', contents)
            self.assertIn('Root node', contents)
            self.assertIn('Chapter 111', contents)

            with open(os.path.join(dir, 'all.html.de')) as f:
                contents = f.read()
            self.assertIn('<html', contents)
            self.assertIn('Kapitel 111', contents)
            self.assertIn('Chapter 2', contents)
