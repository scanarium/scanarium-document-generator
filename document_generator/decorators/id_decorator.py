from .decorator import Decorator


class IdDecorator(Decorator):
    def decorate_node_enter(self, node, state):
        if node['files']:
            state['id'] = node['files']['default']['content-properties']['id']

    def decorate_file(self, file, state):
        file['id'] = state['id']
