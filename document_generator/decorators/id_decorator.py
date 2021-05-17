from .decorator import Decorator


class IdDecorator(Decorator):
    def decorate_node_enter(self, node, state):
        if node['files']:
            try:
                id = node['files']['default']['properties']['id']
            except KeyError:
                self.add_error(
                    state,
                    f'Node `{node["name"]}` is missing the `id` property')
                id = 'anonymous'
            state['id'] = id

    def decorate_file(self, file, state):
        file['id'] = state['id']
