from .decorator import Decorator


class IdDecorator(Decorator):
    def init_state(self):
        state = super().init_state()
        state['seen-ids'] = {}
        return state

    def decorate_node_enter(self, node, state):
        if node['files']:
            try:
                id = node['files']['default']['properties']['id']
            except KeyError:
                self.add_error(
                    state,
                    f'Node `{node["name"]}` is missing the `id` property')
                id = 'anonymous'
            if id in state['seen-ids']:
                self.add_error(
                    state,
                    f'Nodes `{state["seen-ids"][id]}` and `{node["name"]}` '
                    f'have the same `id` `{id}`, although `id`s should be '
                    'unique')

            state['id'] = id
            state['seen-ids'][id] = node["name"]

    def decorate_file(self, file, state):
        file['id'] = state['id']
