import os

from .all_in_one_exporter import AllInOneExporter
from .parser import Parser
from .resource_exporter import ResourceExporter
from .decorators import DefaultFileNodeDecorator
from .decorators import HeaderFileDecorator
from .decorators import IdDecorator
from .decorators import LevelDecorator
from .decorators import MarkdownPropertyExtractorFileDecorator
from .decorators import PropertyDecorator
from .decorators import ValueInjectorFileDecorator


class DocumentGenerator(object):
    def run(self, conf):
        markdown_dir = conf['source']
        output_dir = conf['target']
        default_l10n = conf['default_l10n']
        other_l10ns = conf['additional_l10ns']

        parser = Parser()
        root_node = parser.parse(markdown_dir)

        for decorator in [
            MarkdownPropertyExtractorFileDecorator(),
            LevelDecorator(),
            DefaultFileNodeDecorator(default_l10n),
            PropertyDecorator(),
            IdDecorator(),
            ValueInjectorFileDecorator(
                macros=conf.get('macros', {}),
                external_functions=conf.get('external_functions', {}),
                ),
            HeaderFileDecorator(),
        ]:
            state = decorator.init_state()
            decorator.run(root_node, state)

        os.makedirs(output_dir, exist_ok=True)

        ResourceExporter(conf.get('resources', []), output_dir).export()

        AllInOneExporter(root_node, output_dir, default_l10n, other_l10ns,
                         conf.get('exporter', [])).export()
