from tests import DocumentPageTestCase
from document_generator.decorators import Decorator


class StubDecorator(Decorator):
    def __init__(self):
        super().__init__()
        self.visited = []
        self.warn_on_enter = 0
        self.warn_on_file = 0
        self.warn_on_exit = 0
        self.error_on_enter = 0
        self.error_on_file = 0
        self.error_on_exit = 0
        self.raise_on_enter = 0
        self.raise_on_file = 0
        self.raise_on_exit = 0

    def init_state(self):
        state = super().init_state()
        state['number'] = 42
        return state

    def mark_visited(self, action, name, state):
        self.visited.append(f'{action}-{name} (state: {state["number"]})')

    def decorate_node_enter(self, node, state):
        state['number'] += 1
        if (state['number'] == self.warn_on_enter):
            self.add_warning(state, f'node-enter {node["name"]}')
        if (state['number'] == self.error_on_enter):
            self.add_error(state, f'node-enter {node["name"]}')
        if (state['number'] == self.raise_on_enter):
            raise RuntimeError(f'node-enter {node["name"]}')
        self.mark_visited('node-enter', node['name'], state)

    def decorate_file(self, file, state):
        if (state['number'] == self.warn_on_file):
            self.add_warning(state, f'file {file["markdown"]}')
        if (state['number'] == self.error_on_file):
            self.add_error(state, f'file {file["markdown"]}')
        if (state['number'] == self.raise_on_file):
            raise RuntimeError(f'file {file["markdown"]}')
        self.mark_visited('file', file['markdown'], state)

    def decorate_node_exit(self, node, state):
        if (state['number'] == self.warn_on_exit):
            self.add_warning(state, f'node-exit {node["name"]}')
        if (state['number'] == self.error_on_exit):
            self.add_error(state, f'node-exit {node["name"]}')
        if (state['number'] == self.raise_on_exit):
            raise RuntimeError(f'node-exit {node["name"]}')
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

        messages = decorator.get_messages(state)
        self.assertEqual(len(messages), 0)

    def test_warning_enter(self):
        node1 = {
            'name': 'node1',
            'files': {
            },
            'subnodes': [],
        }
        decorator = StubDecorator()
        decorator.warn_on_enter = 43
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertEqual(messages[0]['text'], 'node-enter node1')
        self.assertEqual(messages[0]['kind'], 'warning')
        self.assertEqual(len(messages), 1)

    def test_warning_exit(self):
        node1 = {
            'name': 'node1',
            'files': {
            },
            'subnodes': [],
        }
        decorator = StubDecorator()
        decorator.warn_on_exit = 43
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertEqual(messages[0]['text'], 'node-exit node1')
        self.assertEqual(messages[0]['kind'], 'warning')
        self.assertEqual(len(messages), 1)

    def test_warning_file(self):
        node1 = {
            'name': 'node1',
            'files': {
                'en': {
                    'markdown': 'en',
                    },
            },
            'subnodes': [],
        }
        decorator = StubDecorator()
        decorator.warn_on_file = 43
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertEqual(messages[0]['text'], 'file en')
        self.assertEqual(messages[0]['kind'], 'warning')
        self.assertEqual(len(messages), 1)

    def test_error_enter(self):
        node1 = {
            'name': 'node1',
            'files': {
            },
            'subnodes': [],
        }
        decorator = StubDecorator()
        decorator.error_on_enter = 43
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertEqual(messages[0]['text'], 'node-enter node1')
        self.assertEqual(messages[0]['kind'], 'error')
        self.assertEqual(len(messages), 1)

    def test_error_exit(self):
        node1 = {
            'name': 'node1',
            'files': {
            },
            'subnodes': [],
        }
        decorator = StubDecorator()
        decorator.error_on_exit = 43
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertEqual(messages[0]['text'], 'node-exit node1')
        self.assertEqual(messages[0]['kind'], 'error')
        self.assertEqual(len(messages), 1)

    def test_error_file(self):
        node1 = {
            'name': 'node1',
            'files': {
                'en': {
                    'markdown': 'en',
                    },
            },
            'subnodes': [],
        }
        decorator = StubDecorator()
        decorator.error_on_file = 43
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertEqual(messages[0]['text'], 'file en')
        self.assertEqual(messages[0]['kind'], 'error')
        self.assertEqual(len(messages), 1)

    def test_warning_error_mix(self):
        node11 = {
            'name': 'node11',
            'files': {
                'de': {
                    'markdown': 'de',
                    },
            },
            'subnodes': [],
        }
        node1 = {
            'name': 'node1',
            'files': {
                'en': {
                    'markdown': 'en',
                    },
            },
            'subnodes': [node11],
        }
        decorator = StubDecorator()
        decorator.warn_on_enter = 44
        decorator.error_on_file = 43
        decorator.warn_on_exit = 43
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertEqual(messages[0]['text'], 'file en')
        self.assertEqual(messages[0]['kind'], 'error')
        self.assertEqual(messages[1]['text'], 'node-enter node11')
        self.assertEqual(messages[1]['kind'], 'warning')
        self.assertEqual(messages[2]['text'], 'node-exit node1')
        self.assertEqual(messages[2]['kind'], 'warning')
        self.assertEqual(len(messages), 3)

    def test_raise_enter(self):
        node1 = {
            'name': 'node1',
            'files': {
            },
            'subnodes': [],
        }
        decorator = StubDecorator()
        decorator.raise_on_enter = 43
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertIn('node-enter node1', messages[0]['text'])
        self.assertEqual(messages[0]['kind'], 'error')
        self.assertEqual(len(messages), 1)

    def test_raise_exit(self):
        node1 = {
            'name': 'node1',
            'files': {
            },
            'subnodes': [],
        }
        decorator = StubDecorator()
        decorator.raise_on_exit = 43
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertIn('node-exit node1', messages[0]['text'])
        self.assertEqual(messages[0]['kind'], 'error')
        self.assertEqual(len(messages), 1)

    def test_raise_file(self):
        node1 = {
            'name': 'node1',
            'files': {
                'en': {
                    'markdown': 'en',
                    },
            },
            'subnodes': [],
        }
        decorator = StubDecorator()
        decorator.raise_on_file = 43
        state = decorator.init_state()
        decorator.run(node1, state)

        messages = decorator.get_messages(state)
        self.assertIn('file en', messages[0]['text'])
        self.assertEqual(messages[0]['kind'], 'error')
        self.assertEqual(len(messages), 1)
