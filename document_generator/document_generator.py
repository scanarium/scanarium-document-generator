import os
import sys

from .all_in_one_exporter import AllInOneExporter
from .build_properties import BuildProperties
from .parser import Parser
from .resource_exporter import ResourceExporter
from .decorators import DebugFileDecorator
from .decorators import DefaultFileNodeDecorator
from .decorators import HeaderFileDecorator
from .decorators import IdDecorator
from .decorators import LevelDecorator
from .decorators import MarkdownPropertyExtractorFileDecorator
from .decorators import PropertyDecorator
from .decorators import ValueInjectorFileDecorator
from .decorators import VersionCheckDecorator


class DocumentGenerator(object):
    def print_message(self, message, target=sys.stderr):
        print('', file=target)
        print(message['kind'], file=target)
        print('  node: ' + message['node']['name'], file=target)
        print('  decorator: ' + message['decorator'].__class__.__name__,
              file=target)
        if 'file' in message:
            print('  file: ' + message['file']['key'], file=target)
        print('  ' + message['text'], file=target)

    def run(self, conf, stderr=sys.stderr):
        markdown_dir = conf['source']
        output_dir = conf['target']
        default_l10n = conf['default_l10n']
        other_l10ns = conf['additional_l10ns']
        l10ns = [default_l10n] + other_l10ns

        parser = Parser()
        root_node = parser.parse(markdown_dir)

        errors = 0
        states = {}
        for decorator in [
            MarkdownPropertyExtractorFileDecorator(),
            LevelDecorator(),
            DefaultFileNodeDecorator(default_l10n),
            PropertyDecorator(BuildProperties(
                markdown_dir, l10ns).getProperties()),
            IdDecorator(),
            VersionCheckDecorator(),
            ValueInjectorFileDecorator(
                macros=conf.get('macros', {}),
                external_functions=conf.get('external_functions', {}),
                ),
            HeaderFileDecorator(),
            DebugFileDecorator(conf.get('debug', False)),
        ]:
            state = decorator.init_state(root_node)
            decorator.run(root_node, state)
            for message in decorator.get_messages(state):
                self.print_message(message, target=stderr)
                if message['kind'] != 'warning':
                    errors += 1
            states[decorator] = state

        os.makedirs(output_dir, exist_ok=True)

        ResourceExporter(conf.get('resources', []), output_dir).export()

        value_injector = None
        value_injector_state = None
        for decorator, state in states.items():
            if isinstance(decorator, ValueInjectorFileDecorator):
                value_injector = decorator
                value_injector_state = state

        AllInOneExporter(
            root_node, output_dir, default_l10n, other_l10ns,
            conf.get('exporter', []), value_injector, value_injector_state
            ).export()

        return errors
