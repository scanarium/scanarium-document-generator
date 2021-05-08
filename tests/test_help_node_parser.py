import os

from .environment import HelpPageTestCase
from help_generator import HelpNodeParser, HelpFileParser

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'help-node-parser')


class HelpNodeParserTest(HelpPageTestCase):
    def parse_fixture(self, name):
        fixture_file = os.path.join(FIXTURE_DIR, name)

        parser = HelpNodeParser(HelpFileParser())

        return parser.parse(fixture_file)

    def test_simple(self):
        actual = self.parse_fixture('simple')

        self.assertTrue(actual['name'].endswith('simple'))

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
