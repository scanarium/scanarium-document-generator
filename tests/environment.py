import os
import unittest


class DocumentPageTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def assertFileExists(self, *args):
        path = os.path.join(*args)
        self.assertTrue(os.path.isfile(path),
                        f'File "{path}" does not exist')
