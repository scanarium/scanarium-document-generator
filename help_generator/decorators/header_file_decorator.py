from .file_decorator import FileDecorator


class HeaderFileDecorator(FileDecorator):
    def decorate_file(self, file, state):
        lines = file['markdown'].split('\n')
        if lines:
            header = lines[0].strip(' #')
            if not header:
                header = file['id']
            header = ('#' * file['level']) + ' ' + header
            header += f" {{: #{file['id']}}}"
            lines[0] = header
            file['markdown'] = '\n'.join(lines)
