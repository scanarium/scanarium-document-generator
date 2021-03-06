from .decorator import Decorator


class LevelDecorator(Decorator):
    def init_state(self, node):
        state = super().init_state(node)
        state['level'] = 0
        return state

    def decorate_node_enter(self, node, state):
        state['level'] += 1

    def decorate_node_exit(self, node, state):
        state['level'] -= 1

    def decorate_file(self, file, state):
        file['level'] = state['level']
