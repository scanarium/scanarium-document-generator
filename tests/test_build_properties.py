import os
import re

from .environment import DocumentPageTestCase
from document_generator import BuildProperties

FIXTURE_DIR = os.path.join('tests', 'fixtures')


class BuildPropertiesTest(DocumentPageTestCase):
    def test_properties(self):
        properties = BuildProperties(
            FIXTURE_DIR, ['foo', 'bar']).getProperties()

        seconds = float(properties['build_seconds_since_epoch'])
        self.assertGreater(seconds, 1620822576)

        year, _, _ = properties['build_day_iso'].split('-')
        self.assertGreater(int(year), 2020)

        self.assertIsNotNone(re.search(r'[0-9a-f]{7}',
                                       properties['build_git_description']))

        self.assertEqual(properties['build_localizations'], 'foo,bar')
