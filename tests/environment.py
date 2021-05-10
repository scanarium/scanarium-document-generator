import os
import tempfile
import unittest


class DocumentPageTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def tempDir(self):
        return tempfile.TemporaryDirectory(prefix='document-generator-test-')

    def assertFileExists(self, *args):
        path = os.path.join(*args)
        self.assertTrue(os.path.isfile(path),
                        f'File "{path}" does not exist')

    def assertStartsWith(self, haystack, needle):
        self.assertTrue(haystack.startswith(needle),
                        f'"{haystack}" does not start with "{needle}"')

    def assertEndsWith(self, haystack, needle):
        self.assertTrue(haystack.endswith(needle),
                        f'"{haystack}" does not end with "{needle}"')
