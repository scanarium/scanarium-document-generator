import os

from .environment import DocumentPageTestCase
from document_generator import ResourceExporter

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'document-node-parser')


class ResourceExporterTest(DocumentPageTestCase):
    def test_empty(self):
        with self.tempDir() as dir:
            exporter = ResourceExporter([], dir)
            exporter.export()

            self.assertEmpty(os.listdir(dir))

    def test_single_string(self):
        with self.tempDir() as dir:
            source_dir = os.path.join(
                FIXTURE_DIR, 'simple', '20-second chapter')
            exporter = ResourceExporter([source_dir], dir)
            exporter.export()

            self.assertFileExists(dir, '20-second chapter', 'en.md')
            self.assertLenIs(os.listdir(dir), 1)

    def test_wildcard(self):
        with self.tempDir() as dir:
            source_dir = os.path.join(
                FIXTURE_DIR, 'simple', '20-second chapter', '*')
            exporter = ResourceExporter([source_dir], dir)
            exporter.export()

            self.assertFileExists(dir, 'en.md')
            self.assertLenIs(os.listdir(dir), 1)
