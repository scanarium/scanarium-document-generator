import os
import subprocess
import tempfile

from .environment import HelpPageTestCase

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'help-node-parser')


class HelpGeneratorTest(HelpPageTestCase):
    def run_command(self, command):
        process = subprocess.run(command,
                                 check=True,
                                 timeout=3,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        return {
            'stdout': process.stdout,
            'stderr': process.stderr,
        }

    def test_simple(self):
        with tempfile.TemporaryDirectory(prefix='help-generator-test-') as dir:
            command = [
                os.path.join('.', 'generator.py'),
                '--source', os.path.join(FIXTURE_DIR, 'simple'),
                '--target', dir,
                '--additional-localizations', 'de',
            ]
            self.run_command(command)

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