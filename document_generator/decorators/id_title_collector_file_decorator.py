from .file_decorator import FileDecorator
from .utils import Utils


class IdTitleCollectorFileDecorator(FileDecorator):
    def __init__(self, initial_state={}):
        self.utils = Utils()
        self.initial_state = initial_state

    def init_state(self, node):
        state = super().init_state(node)
        state['id-title-map'] = {}
        return state

    def decorate_file(self, file, state):
        title = self.utils.extract_title(file['markdown'])

        if not title:
            title = '(anonymous)'
            self.add_error(state, 'Failed to determine title')

        id_title_map = state['id-title-map']
        id = file['id']
        if id not in id_title_map:
            id_title_map[id] = {}
        key = 'default' if file.get('is-default', False) else file['key']
        id_title_map[id][key] = title
