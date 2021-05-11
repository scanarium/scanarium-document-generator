from .file_decorator import FileDecorator


class MarkdownPropertyExtractorFileDecorator(FileDecorator):
    def decorate_file(self, file, state):
        properties = {}

        lines = file['markdown'].split('\n')

        # Trim trailing empty lines
        keep_searching = lines
        while keep_searching:
            line = lines[-1]
            if line:
                keep_searching = False
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    if key and not key.strip('abcdefghijklmnopqrstuvwxyz-'):
                        properties[key] = value.strip()
                        keep_searching = True
                else:
                    keep_searching = not line.strip()

            if keep_searching:
                del lines[-1]
                keep_searching = lines

        # Trim trailing empty lines again, now that we cho
        while lines and not lines[-1]:
            lines = lines[:-1]

        file['markdown'] = '\n'.join(lines) + ('\n' if lines else '')
        file['markdown-properties'] = properties
