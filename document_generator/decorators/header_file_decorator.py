from .file_decorator import FileDecorator


class HeaderFileDecorator(FileDecorator):
    def decorate_file(self, file, state):
        lines = file['markdown'].split('\n')
        if lines:
            header = lines[0].strip(' #')
            if not header:
                header = file['id']
            header = ('#' * file['level']) + ' ' + header
            attribute_str = f"#{file['id']}"
            if '{:' in header:
                left, right = header.split('{:', 1)
                header = left + '{: ' + attribute_str + ' ' + right
                if '}' not in right:
                    header += '}'
            else:
                header += f" {{: {attribute_str}}}"
            lines[0] = header
            file['markdown'] = '\n'.join(lines)
