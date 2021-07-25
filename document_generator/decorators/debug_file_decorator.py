from .file_decorator import FileDecorator


class DebugFileDecorator(FileDecorator):
    def __init__(self, enabled):
        self.enabled = enabled

    def decorate_file(self, file, state):
        if self.enabled:
            markdown = file['markdown'].split('\n')
            file_name = file['file_name']
            content = [
                '',
                f'id: {file["id"]}', '{: class=debug-node-id}',
                '',
                f'{file_name}', '{: class=debug-source-file}',
                '',
                ]
            file['markdown'] = '\n'.join(
                [markdown[0]] + content + markdown[1:])
