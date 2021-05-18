from .file_decorator import FileDecorator


class IdTitleCollectorFileDecorator(FileDecorator):
    def init_state(self, node):
        state = super().init_state(node)
        state['id-title-map'] = {}
        return state

    def decorate_file(self, file, state):
        markdown_lines = file['markdown'].split('\n')
        title = ''
        while not title and markdown_lines:
            title = markdown_lines[0].strip()
            del markdown_lines[0]

        if not title:
            title = '(anonymous)'
            self.add_error(state, 'Failed to determine title')

        while title.startswith('#'):
            title = title[1:].strip()

        title = title.split('{:', 1)[0].strip()

        id_title_map = state['id-title-map']
        id = file['id']
        if id not in id_title_map:
            id_title_map[id] = {}
        key = 'default' if file.get('is-default', False) else file['key']
        id_title_map[id][key] = title
