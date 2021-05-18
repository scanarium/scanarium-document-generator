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
        if not os.path.isfile(path):
            self.fail(f'File "{path}" does not exist')

    def assertStartsWith(self, haystack, needle):
        if not haystack.startswith(needle):
            self.fail(f'"{haystack}" does not start with "{needle}"')

    def assertEndsWith(self, haystack, needle):
        if not haystack.endswith(needle):
            self.fail(f'"{haystack}" does not end with "{needle}"')

    def assertEmpty(self, lst):
        if len(lst):
            self.fail(f'List should be empty, but is "{lst}"')

    def assertLenIs(self, lst, n):
        if len(lst) != n:
            self.fail(f'Length {n} expected, but length is {len(lst)} for '
                      f'"{lst}"')
