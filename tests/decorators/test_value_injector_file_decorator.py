from tests import DocumentPageTestCase
from document_generator.decorators import ValueInjectorFileDecorator


class ValueInjectorFileDecoratorTest(DocumentPageTestCase):
    def assertInjectedMarkdown(self, markdown, properties, expected):
        file = {
            "markdown": markdown,
            "properties": properties,
            }

        decorator = ValueInjectorFileDecorator()
        state = decorator.init_state()
        decorator.decorate_file(file, state)

        self.assertEqual(file["markdown"], expected)

    def test_empty(self):
        self.assertInjectedMarkdown("", {}, "")

    def test_no_properties(self):
        self.assertInjectedMarkdown("foo", {}, "foo")

    def test_undefined_property(self):
        self.assertInjectedMarkdown(
            "foo{=property(bar)}baz",
            {},
            "foo{=property(bar)}baz")

    def test_plain_property(self):
        self.assertInjectedMarkdown(
            "foo{=property(bar)}baz",
            {"bar": "BAR"},
            "fooBARbaz")

    def test_spaced_property(self):
        self.assertInjectedMarkdown(
            "foo{   =   property(   bar  )  }baz",
            {"bar": "BAR"},
            "fooBARbaz")

    def test_property_at_beginning(self):
        self.assertInjectedMarkdown(
            "{=property(bar)}baz",
            {"bar": "BAR"},
            "BARbaz")

    def test_property_at_end(self):
        self.assertInjectedMarkdown(
            "foo{=property(bar)}",
            {"bar": "BAR"},
            "fooBAR")

    def test_property_chain(self):
        self.assertInjectedMarkdown(
            "foo{=property(bar)}baz",
            {
                "bar": "{=property(quux)}-",
                "quux": "-{=property(quuux)}",
                "quuux": "QUUUX",
            },
            "foo-QUUUX-baz")

    def test_property_indirect(self):
        self.assertInjectedMarkdown(
            "foo-{=property({=property(bar)})}-baz",
            {
                "bar": "foo",
                "foo": "QUUUX",
            },
            "foo-QUUUX-baz")

    def test_property_idempotence(self):
        self.assertInjectedMarkdown(
            "foo-{=property(bar)}-baz",
            {
                "bar": "{=property(bar)}",
            },
            "foo-{=property(bar)}-baz")

    def test_property_loops(self):
        self.assertInjectedMarkdown(
            "foo-{=property(bar)}-baz",
            {
                "bar": "{=property(quux)}",
                "quux1": "{=property(quux2)}",
                "quux2": "{=property(quux3)}",
                "quux3": "{=property(quux4)}",
                "quux4": "{=property(quux1)}",
                "QUUUX": "{=property(quux)}",
            },
            "foo-{=property(quux)}-baz")
