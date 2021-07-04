from tests import DocumentPageTestCase
from document_generator.decorators import Utils


class DefaultFileNodeDecoratorTest(DocumentPageTestCase):
    def test_update_dict_empty(self):
        target = {}
        update = {
            'number': 2,
            'string': 'abc',
            'dict': {
                'foo': 'bar',
                }
            }
        actual = Utils().update_dict(target, update)

        self.assertEqual(actual, target)
        self.assertEqual(actual, {
            'number': 2,
            'string': 'abc',
            'dict': {
                'foo': 'bar',
                }
            })

    def test_update_number(self):
        target = {'number': 1}
        update = {
            'number': 2,
            }
        actual = Utils().update_dict(target, update)

        self.assertEqual(actual, target)
        self.assertEqual(actual, {
            'number': 2,
            })

    def test_update_string(self):
        target = {'string': 'foo'}
        update = {
            'string': 'bar',
            }
        actual = Utils().update_dict(target, update)

        self.assertEqual(actual, target)
        self.assertEqual(actual, {
            'string': 'bar',
            })

    def test_update_dict(self):
        target = {
            'foo': {
                'bar': {
                    'baz': 1,
                    'quux': 'quuux',
                    'foo': 'bar',
                    },
                'aaa': 'bbb',
                'fooaaa': 'baraaa',
                },
            'xxx': 'yyy',
            'fooxxx': 'barxxx',
            }
        update = {
            'foo': {
                'bar': {
                    'baz': 2,
                    'quux': 'qUUUx',
                    },
                'aaa': 'BBB',
                },
            'xxx': 'YYY',
            'zzz': 'ZZZ',
            }
        actual = Utils().update_dict(target, update)

        self.assertEqual(actual, target)
        self.assertEqual(actual, {
                'foo': {
                    'bar': {
                        'baz': 2,
                        'quux': 'qUUUx',
                        'foo': 'bar',
                        },
                    'aaa': 'BBB',
                    'fooaaa': 'baraaa',
                    },
                'xxx': 'YYY',
                'fooxxx': 'barxxx',
                'zzz': 'ZZZ',
                })

    def test_extract_title_empty(self):
        actual = Utils().extract_title('')
        self.assertEqual(actual, '')

    def test_extract_title_only_title(self):
        actual = Utils().extract_title('foo')
        self.assertEqual(actual, 'foo')

    def test_extract_title_paragraphs(self):
        actual = Utils().extract_title('foo\n\nbar')
        self.assertEqual(actual, 'foo')

    def test_extract_title_multiline(self):
        actual = Utils().extract_title('foo\nbar')
        self.assertEqual(actual, 'foo')

    def test_extract_title_marker_stripping(self):
        actual = Utils().extract_title('## # # foo\nbar')
        self.assertEqual(actual, 'foo')

    def test_extract_title_attribute_stripping(self):
        actual = Utils().extract_title('foo {: class=quux}\nbar')
        self.assertEqual(actual, 'foo')
