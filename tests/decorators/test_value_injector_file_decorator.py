from tests import DocumentPageTestCase
from document_generator.decorators import ValueInjectorFileDecorator


class ValueInjectorFileDecoratorTest(DocumentPageTestCase):
    def assertInjectedMarkdown(self, markdown, expected, properties={},
                               macros={}):
        file = {
            'markdown': markdown,
            'properties': properties,
            }

        decorator = ValueInjectorFileDecorator(macros=macros)
        state = decorator.init_state()
        decorator.decorate_file(file, state)

        self.assertEqual(file['markdown'], expected)

    def test_empty(self):
        self.assertInjectedMarkdown('', '', {})

    def test_no_properties(self):
        self.assertInjectedMarkdown('foo', 'foo', {})

    def test_undefined_property(self):
        self.assertInjectedMarkdown(
            'foo{=property(bar)}baz',
            'foo{=property(bar)}baz',
            {})

    def test_plain_property(self):
        self.assertInjectedMarkdown(
            'foo{=property(bar)}baz',
            'fooBARbaz',
            {'bar': 'BAR'})

    def test_spaced_property(self):
        self.assertInjectedMarkdown(
            'foo{   =   property(   bar  )  }baz',
            'fooBARbaz',
            {'bar': 'BAR'})

    def test_property_at_beginning(self):
        self.assertInjectedMarkdown(
            '{=property(bar)}baz',
            'BARbaz',
            {'bar': 'BAR'})

    def test_property_at_end(self):
        self.assertInjectedMarkdown(
            'foo{=property(bar)}',
            'fooBAR',
            {'bar': 'BAR'})

    def test_property_chain(self):
        self.assertInjectedMarkdown(
            'foo{=property(bar)}baz',
            'foo-QUUUX-baz',
            {
                'bar': '{=property(quux)}-',
                'quux': '-{=property(quuux)}',
                'quuux': 'QUUUX',
            })

    def test_property_indirect(self):
        self.assertInjectedMarkdown(
            'foo-{=property({=property(bar)})}-baz',
            'foo-QUUUX-baz',
            {
                'bar': 'foo',
                'foo': 'QUUUX',
            })

    def test_property_idempotence(self):
        self.assertInjectedMarkdown(
            'foo-{=property(bar)}-baz',
            'foo-{=property(bar)}-baz',
            {
                'bar': '{=property(bar)}',
            })

    def test_property_loops(self):
        self.assertInjectedMarkdown(
            'foo-{=property(bar)}-baz',
            'foo-{=property(quux)}-baz',
            {
                'bar': '{=property(quux)}',
                'quux1': '{=property(quux2)}',
                'quux2': '{=property(quux3)}',
                'quux3': '{=property(quux4)}',
                'quux4': '{=property(quux1)}',
                'QUUUX': '{=property(quux)}',
            })

    def test_macro_undefined(self):
        self.assertInjectedMarkdown(
            'foo-{=macro(bar)}-baz',
            'foo-{=macro(bar)}-baz')

    def test_macro_simple(self):
        self.assertInjectedMarkdown(
            'foo-{=macro(bar)}-baz',
            'foo-quux-baz',
            macros={'bar': 'quux'})

    def test_macro_simple_one_argument(self):
        self.assertInjectedMarkdown(
            'foo-{=macro(bar, -)}-baz-{=macro(bar, +)}',
            'foo-q-u-u-x-baz-q+u+u+x',
            macros={'bar': 'q$1u$1u$1x'})

    def test_macro_simple_multiple_arguments(self):
        self.assertInjectedMarkdown(
            'foo-{=macro(bar, -, .oOo., +)}-baz',
            'foo-q-u.oOo.u+x-baz',
            macros={'bar': 'q$1u$2u$3x'})

    def test_macro_simple_mixed_simple_property_inside(self):
        self.assertInjectedMarkdown(
            '{=macro({=property(foo)}, a)}',
            'baz',
            properties={'foo': 'bar'},
            macros={'bar': 'b$1z'})

    def test_macro_simple_mixed_simple_macro_inside(self):
        self.assertInjectedMarkdown(
            '{=property({=macro(bar, o)})}',
            'baz',
            properties={'foo': 'baz'},
            macros={'bar': 'f$1o'})

    def test_macro_line_break(self):
        self.assertInjectedMarkdown(
            '{=macro(foo, bar, baz)}',
            'bar\nbaz',
            macros={'foo': '$1\\n$2'})

    def test_macro_wildcard_no_arguments(self):
        self.assertInjectedMarkdown(
            '{=macro(foo)}',
            '||',
            macros={'foo': '|$*|'})

    def test_macro_wildcard_single_argument(self):
        self.assertInjectedMarkdown(
            '{=macro(foo, bar)}',
            '|bar|',
            macros={'foo': '|$*|'})

    def test_macro_wildcard_multiple_arguments(self):
        self.assertInjectedMarkdown(
            '{=macro(foo, bar,baz, quux,  quuux)}',
            '|bar, baz, quux, quuux|',
            macros={'foo': '|$*|'})
