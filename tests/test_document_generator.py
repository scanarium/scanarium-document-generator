import io
import os

from .environment import DocumentPageTestCase
from document_generator import DocumentGenerator

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'document-node-parser')


class DocumentGeneratorTest(DocumentPageTestCase):
    def test_simple(self):
        with self.tempDir() as dir:
            fixture_dir = os.path.join(FIXTURE_DIR, 'simple')
            generator = DocumentGenerator()
            errors = generator.run({
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

            self.assertNotIn(os.path.join('simple', 'en.md'), contents)

            self.assertEqual(0, errors)

    def test_missing_id(self):
        with self.tempDir() as dir:
            fixture_dir = os.path.join(FIXTURE_DIR, 'missing-id')
            generator = DocumentGenerator()
            capture = io.StringIO()
            errors = generator.run({
                    'source': fixture_dir,
                    'target': dir,
                    'default_l10n': 'en',
                    'additional_l10ns': ['de'],
                    'debug': True,
                    }, stderr=capture)

            with open(os.path.join(dir, 'all.html.en')) as f:
                contents = f.read()
            self.assertIn('id="anonymous"', contents)
            self.assertIn('id="chapter-2"', contents)
            self.assertIn(os.path.join('missing-id', '10-chapter', 'en.md'),
                          contents)

            stderr = capture.getvalue()
            self.assertIn('error', stderr)
            self.assertIn('missing', stderr)
            self.assertEqual(1, errors)
