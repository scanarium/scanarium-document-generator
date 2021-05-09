import os

from .all_in_one_exporter import AllInOneExporter
from .parser import Parser


class HelpGenerator(object):
    def run(self, help_root_dir, output_dir, default_l10n, other_l10ns):
        parser = Parser()
        root_node = parser.parse(help_root_dir)

        os.makedirs(output_dir, exist_ok=True)

        AllInOneExporter(root_node, output_dir, default_l10n, other_l10ns
                         ).export()
