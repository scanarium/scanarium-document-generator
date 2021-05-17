from tests import DocumentPageTestCase
from document_generator.decorators import FileDecorator


class StubDecorator(FileDecorator):
    def __init__(self):
        super().__init__()
        self.visited = []

    def init_state(self):
        state = super().init_state()
        state['number'] = 42
        return state

    def mark_visited(self, action, name, state):
        self.visited.append(f'{action}-{name} (state: {state["number"]})')

    def decorate_file(self, node, state):
        self.mark_visited('file', node['markdown'], state)
        state['number'] += 1


class FileDecoratorTest(DocumentPageTestCase):
    def test_simple(self):
        node111 = {
            'name': 'node111',
            'files': {
                'en': {
                    'markdown': '111-fooEn',
                    },
                'de': {
                    'markdown': '111-fooDe',
                    },
            },
            'subnodes': [],
        }
        node11 = {
            'name': 'node11',
            'files': {},
            'subnodes': [node111],
        }
        node12 = {
            'name': 'node12',
            'files': {},
            'subnodes': [],
        }
        node1 = {
            'name': 'node1',
            'files': {
                'en': {
                    'markdown': '1-barEn'
                    },
                'eo': {
                    'markdown': '1-barEo'
                    },
            },
            'subnodes': [node11, node12],
        }

        decorator = StubDecorator()
        state = decorator.init_state()
        decorator.run(node1, state)

        self.assertEqual(decorator.visited, [
                "file-1-barEn (state: 42)",
                "file-1-barEo (state: 43)",
                "file-111-fooDe (state: 44)",
                "file-111-fooEn (state: 45)",
                ])
