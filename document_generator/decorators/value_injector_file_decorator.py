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
        counter = -1

        def replacement(match):
            nonlocal counter
            ret = match.group(0)
            func_name = match.group(1)
            try:
                func = self.funcs[func_name]
                args = [x.strip() for x in match.group(2).split(',')]
                ret = func(file, state, args)
                counter += 1
            except Exception:
                # Substitution failed
                pass

            return ret

        while counter:
            counter = 0
            file['markdown'] = re.sub(
                r'{\s*=\s*([a-z]+)\s*\(([^){]*)\)\s*}',
                replacement,
                file['markdown'])
