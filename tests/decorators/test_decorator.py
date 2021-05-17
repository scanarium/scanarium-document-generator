from tests import DocumentPageTestCase
from document_generator.decorators import Decorator


class StubDecorator(Decorator):
    def __init__(self):
        super().__init__()
        self.visited = []

    def init_state(self):
        state = super().init_state()
        state['number'] = 42
        return state

    def mark_visited(self, action, name, state):
        self.visited.append(f'{action}-{name} (state: {state["number"]})')

    def decorate_node_enter(self, node, state):
        state['number'] += 1
        self.mark_visited('node-enter', node['name'], state)

    def decorate_file(self, file, state):
        self.mark_visited('file', file['markdown'], state)

    def decorate_node_exit(self, node, state):
        self.mark_visited('node-exit', node['name'], state)
        state['number'] -= 1


class DecoratorTest(DocumentPageTestCase):
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
                "node-enter-node1 (state: 43)",
                "file-1-barEn (state: 43)",
                "file-1-barEo (state: 43)",
                "node-enter-node11 (state: 44)",
                "node-enter-node111 (state: 45)",
                "file-111-fooDe (state: 45)",
                "file-111-fooEn (state: 45)",
                "node-exit-node111 (state: 45)",
                "node-exit-node11 (state: 44)",
                "node-enter-node12 (state: 44)",
                "node-exit-node12 (state: 44)",
                "node-exit-node1 (state: 43)",
                ])
