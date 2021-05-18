from tests import DocumentPageTestCase
from document_generator.decorators import HeaderFileDecorator


class HeaderFileDecoratorTest(DocumentPageTestCase):
    def decorate(self, file):
        decorator = HeaderFileDecorator()
        decorator.decorate_file(file, decorator.init_state({}))

    def test_empty(self):
        file = {
            'markdown': '',
            'level': 1,
            'id': 'foo',
            }

        self.decorate(file)

        self.assertEqual(file['markdown'],
                         '# foo {: #foo class=document-generator-node}')

    def test_plain(self):
        file = {
            'markdown': '# Title foo\n\nbar',
            'id': 'idFoo',
            'level': 3,
            }

        self.decorate(file)

        self.assertEqual(file['markdown'],
                         '### Title foo {: #idFoo '
                         'class=document-generator-node}\n\nbar')

    def test_attributes_already_present(self):
        file = {
            'markdown': '# Title foo {:key=value}\n\nbar',
            'id': 'idFoo',
            'level': 1,
            }

        self.decorate(file)

        self.assertEqual(file['markdown'],
                         '# Title foo {: #idFoo class=document-generator-node '
                         'key=value}\n\nbar')

    def test_attributes_already_open_no_end(self):
        file = {
            'markdown': '# Title foo {:key=value\n\nbar',
            'id': 'idFoo',
            'level': 1,
            }

        self.decorate(file)

        self.assertEqual(file['markdown'],
                         '# Title foo {: #idFoo class=document-generator-node '
                         'key=value}\n\nbar')
