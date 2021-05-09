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
                if ':' in line:
                    key, value = line.split(':', 1)
                    properties[key.strip()] = value.strip()
                else:
                    keep_searching = False

            if keep_searching:
                del lines[-1]
                keep_searching = lines

        # Trim trailing empty lines again, now that we cho
        while lines and not lines[-1]:
            lines = lines[:-1]

        file['markdown'] = '\n'.join(lines) + '\n'
        file['markdown-properties'] = properties
