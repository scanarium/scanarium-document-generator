from .decorator import Decorator


class VersionCheckDecorator(Decorator):
    def __init__(self, actions=['error']):
        self.actions = actions

    def init_state(self, node):
        state = super().init_state(node)

        state['parent_versions'] = []

        return state

    def decorate_node_enter(self, node, state):
        node_version = 'n/a'
        if node['files']:
            node_version = node['files']['default']['properties']['version']

        state['parent_versions'].append(node_version)

    def get_major_version(self, version):
        return version.split('.')[0].strip()

    def handle_version_mismatch(self, node_version, file_version, state):
        message = f'Mismatch in major version. Node has {node_version}. ' \
            f'File has {file_version}'
        for action in self.actions:
            action = action.strip()
            if action == 'error':
                self.add_error(state, message)
            elif action == 'warning':
                self.add_warning(state, message)
            else:
                self.add_error(
                    state,
                    f'Unkown action "{action}" in version check decorator')

    def decorate_file(self, file, state):
        if file['key'] != 'properties':
            node_version = state['parent_versions'][-1]
            node_major_version = self.get_major_version(node_version)
            file_version = file['properties']['version']
            file_major_version = self.get_major_version(file_version)
            if node_major_version != file_major_version:
                self.handle_version_mismatch(node_version, file_version, state)

    def decorate_node_exit(self, node, state):
        del state['parent_versions'][-1]
