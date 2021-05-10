import os

from .environment import DocumentPageTestCase
from document_generator import Parser

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'document-node-parser')


class ParserTest(DocumentPageTestCase):
    def parse_fixture(self, name):
        fixture_file = os.path.join(FIXTURE_DIR, name)

        parser = Parser()

        return parser.parse(fixture_file)

    def test_simple(self):
        actual = self.parse_fixture('simple')

        files = actual['files']
        self.assertEqual(files['en']['key'], 'en')
        self.assertEqual(len(files), 1)

        subnodes = actual['subnodes']
        self.assertEqual(len(subnodes[0]['files']), 0)
        self.assertEqual(
            subnodes[0]['subnodes'][0]['files']['de']['key'], 'de')
        self.assertEqual(
            subnodes[0]['subnodes'][0]['files']['en']['key'], 'en')
        self.assertEqual(len(subnodes[0]['subnodes'][0]['files']), 2)
        self.assertEqual(
            subnodes[0]['subnodes'][0]['subnodes'][0]['files']['de']['key'],
            'de')
        self.assertEqual(
            subnodes[0]['subnodes'][0]['subnodes'][0]['files']['en']['key'],
            'en')
        self.assertEqual(
            len(subnodes[0]['subnodes'][0]['subnodes'][0]['files']), 2)
        self.assertEqual(
            len(subnodes[0]['subnodes'][0]['subnodes'][0]['subnodes']), 0)
        self.assertEqual(len(subnodes[0]['subnodes'][0]['subnodes']), 1)
        self.assertEqual(
            subnodes[0]['subnodes'][1]['files']['de']['key'], 'de')
        self.assertEqual(
            subnodes[0]['subnodes'][1]['files']['en']['key'], 'en')
        self.assertEqual(len(subnodes[0]['subnodes'][1]['files']), 2)
        self.assertEqual(len(subnodes[0]['subnodes'][1]['subnodes']), 0)
        self.assertEqual(len(subnodes[0]['subnodes']), 2)
        self.assertEqual(subnodes[1]['files']['en']['key'], 'en')
        self.assertEqual(len(subnodes[1]['files']), 1)
        self.assertEqual(len(subnodes[1]['subnodes']), 0)
