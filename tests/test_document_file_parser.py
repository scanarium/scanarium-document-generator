import os

from .environment import DocumentPageTestCase
from document_generator import DocumentFileParser

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'document-file-parser')


class DocumentFileParserTest(DocumentPageTestCase):
    def parse_fixture(self, name):
        fixture_file = os.path.join(FIXTURE_DIR, f'{name}.md')

        parser = DocumentFileParser()

        return parser.parse(fixture_file)

    def test_key(self):
        actual = self.parse_fixture('only-markdown')
        self.assertEqual(actual['key'], 'only-markdown')

    def test_markdown(self):
        actual = self.parse_fixture('only-markdown')
        self.assertEqual(actual['markdown'], '# Section foo\n\nbar\n')
