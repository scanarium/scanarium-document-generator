import re

from importlib.machinery import SourceFileLoader
from inspect import getmembers, isfunction

from .file_decorator import FileDecorator
from .id_title_collector_file_decorator import IdTitleCollectorFileDecorator


class ValueInjectorFileDecorator(FileDecorator):
    def __init__(self, macros={}, external_functions={}):
        super().__init__()
        self.macros = macros
        self.funcs = {
            "property": self.funcProperty,
            "lower": self.funcLower,
            "macro": self.funcMacro,
            "substring": self.funcSubstring,
            "upper": self.funcUpper,
            "nodeTitle": self.funcNodeTitle,
            }

        for imported_name, import_spec in external_functions.items():
            self.funcs[imported_name] = self.loadExternalFunction(
                imported_name, import_spec)

    def init_state(self, root):
        id_title_collector = IdTitleCollectorFileDecorator()
        id_title_colletor_state = id_title_collector.init_state(root)
        id_title_collector.run(root, id_title_colletor_state)

        state = super().init_state(root)
        state['id-title-map'] = id_title_colletor_state['id-title-map']

        return state

    def loadExternalFunction(self, imported_name, import_spec):
        ret = None

        module = SourceFileLoader(f'value_injector_{imported_name}',
                                  import_spec['file']).load_module()
        for member_name, member_value in getmembers(module, isfunction):
            if member_name == import_spec['name']:
                ret = member_value
        return ret

    def funcLower(self, file, state, args):
        return ', '.join(args).lower()

    def funcProperty(self, file, state, args):
        return file['properties'][args[0]]

    def funcUpper(self, file, state, args):
        return ', '.join(args).upper()

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

    def funcNodeTitle(self, file, state, args):
        id = args[0]
        if len(args) > 1:
            lang = args[1]
        else:
            lang = file['key']

        title_map = state['id-title-map'][id]
        if lang not in title_map:
            lang = 'default'

        return title_map[lang]

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
                r'{\s*=\s*([a-zA-Z0-9]+)\s*\((([^){]|{\s*[^)=\s])*)\)\s*}',
                replacement,
                current)
        file['markdown'] = current

    def decorate_text(self, text, state, key='default', properties={}):
        file = {
            'markdown': text,
            'properties': properties,
            'key': key,
            }

        self.decorate_file(file, state)

        return file['markdown']
