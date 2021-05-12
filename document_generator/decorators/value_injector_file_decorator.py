import re

from importlib.machinery import SourceFileLoader
from inspect import getmembers, isfunction

from .file_decorator import FileDecorator


class ValueInjectorFileDecorator(FileDecorator):
    def __init__(self, macros={}, external_functions={}):
        super().__init__()
        self.macros = macros
        self.funcs = {
            "property": self.funcProperty,
            "macro": self.funcMacro,
            "substring": self.funcSubstring,
            }

        for imported_name, import_spec in external_functions.items():
            self.funcs[imported_name] = self.loadExternalFunction(
                imported_name, import_spec)

    def loadExternalFunction(self, imported_name, import_spec):
        ret = None

        module = SourceFileLoader(f'value_injector_{imported_name}',
                                  import_spec['file']).load_module()
        for member_name, member_value in getmembers(module, isfunction):
            if member_name == import_spec['name']:
                ret = member_value
        return ret

    def funcProperty(self, file, state, args):
        return file['properties'][args[0]]

    def funcMacro(self, file, state, args):
        name = args[0]
        value = self.macros[name]

        # Inject positional arguments
        for i in range(1, len(args)):
            value = value.replace(f'${i}', args[i])

        # Inject wildcard argument
        value = value.replace('$*', ', '.join(args[1:]))

        # Convert encoded JavaScript line-breaks into real line-breaks
        value = value.replace('\\n', '\n')
        return value

    def funcSubstring(self, file, state, args):
        end = int(args[-1]) if args[-1] else None
        start = int(args[-2]) if args[-2] else None
        return ', '.join(args[0:-2])[start:end]

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
