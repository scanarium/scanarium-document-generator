import os
import subprocess

import document_generator

from .environment import DocumentPageTestCase

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'document-node-parser')


class DocumentGeneratorTest(DocumentPageTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.utils = document_generator.Utils()

    def test_simple(self):
        with self.tempDir() as dir:
            command = [
                os.path.join('.', 'generator.py'),
                '--source', os.path.join(FIXTURE_DIR, 'simple'),
                '--target', dir,
                '--additional-localizations', 'de',
            ]
            self.utils.run_command(command)

            with open(os.path.join(dir, 'all.html.en')) as f:
                contents = f.read()
            self.assertIn('<html', contents)
            self.assertIn('Root node', contents)
            self.assertIn('<h3 class="document-generator-node" id="chapter11">'
                          'Chapter 11', contents)
            self.assertIn('Chapter 111', contents)

            with open(os.path.join(dir, 'all.html.de')) as f:
                contents = f.read()
            self.assertIn('<html', contents)
            self.assertIn('<h3 class="document-generator-node" id="chapter11">'
                          'Kapitel 11', contents)
            self.assertIn('Kapitel 111', contents)
            self.assertIn('Chapter 2', contents)

    def test_missing_id(self):
        with self.tempDir() as dir:
            command = [
                os.path.join('.', 'generator.py'),
                '--source', os.path.join(FIXTURE_DIR, 'missing-id'),
                '--target', dir,
                '--additional-localizations', 'de',
            ]
            with self.assertRaises(subprocess.CalledProcessError) as cm:
                self.utils.run_command(command)

            exception = cm.exception
            stderr = exception.stderr
            self.assertIn('error', stderr)
            self.assertIn('missing', stderr)
            self.assertEqual(1, exception.returncode)

    def test_duplicate_id(self):
        with self.tempDir() as dir:
            command = [
                os.path.join('.', 'generator.py'),
                '--source', os.path.join(FIXTURE_DIR, 'duplicate-id'),
                '--target', dir,
            ]
            with self.assertRaises(subprocess.CalledProcessError) as cm:
                self.utils.run_command(command)

            exception = cm.exception
            stderr = exception.stderr
            self.assertIn('error', stderr)
            self.assertIn('this-id-is-duplicated', stderr)
            self.assertEqual(1, exception.returncode)
