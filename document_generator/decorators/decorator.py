class Decorator(object):
    def init_state(self, node):
        return {
            '__decorator': {
                'messages': [],
                }
            }

    def _add_message(self, kind, state, text):
        message = {
            'decorator': self,
            'kind': kind,
            'node': state['__decorator']['node'],
            'text': text,
            }
        if 'file' in state['__decorator']:
            message['file'] = state['__decorator']['file']

        state['__decorator']['messages'].append(message)

    def add_warning(self, state, text):
        self._add_message('warning', state, text)

    def add_error(self, state, text):
        self._add_message('error', state, text)

    def get_messages(self, state):
        return state['__decorator']['messages']

    def decorate_file(self, file, state):
        pass

    def decorate_node_enter(self, node, state):
        pass

    def decorate_node_exit(self, node, state):
        pass

    def call_guarded(self, func, obj, state):
        try:
            func(obj, state)
        except Exception as e:
            self.add_error(state, f'Caught exception {e}')

    def run(self, node, state={}):
        state['__decorator']['node'] = node
        self.call_guarded(self.decorate_node_enter, node, state)

        for file_key in sorted(node['files'].keys()):
            file = node['files'][file_key]
            state['__decorator']['file'] = file
            self.call_guarded(self.decorate_file, file, state)

        try:
            del state['__decorator']['file']
        except KeyError:
            # Node does not have files. Nothing to clean up.
            pass

        for subnode in node['subnodes']:
            self.call_guarded(self.run, subnode, state)
            state['__decorator']['node'] = node

        self.call_guarded(self.decorate_node_exit, node, state)
