from .decorator import Decorator


class DebugFileDecorator(Decorator):
    def __init__(self, enabled):
        self.enabled = enabled

    def decorate_file(self, file, state):
        if self.enabled:
            markdown = file['markdown'].split('\n')
            file_name = file['file_name']
            content = ['', f'{file_name}', '{: class=source-file}', '']
            file['markdown'] = '\n'.join(
                [markdown[0]] + content + markdown[1:])
