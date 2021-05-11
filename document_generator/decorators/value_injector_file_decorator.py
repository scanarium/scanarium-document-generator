import re

from .file_decorator import FileDecorator


class ValueInjectorFileDecorator(FileDecorator):
    def __init__(self):
        super().__init__()
        self.funcs = {
            "property": self.funcProperty,
            }

    def funcProperty(self, file, state, args):
        return file['properties'][args[0]]

    def decorate_file(self, file, state):
        def replacement(match):
            ret = match.group(0)
            func_name = match.group(1)
            try:
                func = self.funcs[func_name]
                args = [x.strip() for x in match.group(2).split(',')]
                ret = func(file, state, args)
            except Exception:
                # Substitution failed
                pass

            return ret

        old_values = []
        current = file['markdown']
        while current not in old_values:
            old_values.append(current)
            current = re.sub(
                r'{\s*=\s*([a-z]+)\s*\(([^){]*)\)\s*}',
                replacement,
                current)
        file['markdown'] = current
