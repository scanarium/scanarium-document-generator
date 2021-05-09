from tests import HelpPageTestCase
from help_generator.decorators import HeaderFileDecorator


class HeaderFileDecoratorTest(HelpPageTestCase):
    def test_empty(self):
        file = {
            'markdown': '',
            'level': 1,
            'id': 'foo',
            }

        decorator = HeaderFileDecorator()
        decorator.decorate_file(file, decorator.init_state())

        self.assertEqual(file['markdown'], '# foo {: #foo}')

    def test_plain(self):
        file = {
            'markdown': '# Title foo\n\nbar',
            'id': 'idFoo',
            'level': 3,
            }

        decorator = HeaderFileDecorator()
        decorator.decorate_file(file, decorator.init_state())

        self.assertEqual(file['markdown'], '### Title foo {: #idFoo}\n\nbar')
