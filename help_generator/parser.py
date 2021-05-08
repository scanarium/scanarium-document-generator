import os

from .help_generator_error import HelpGeneratorError
from .help_file_parser import HelpFileParser
from .help_node_parser import HelpNodeParser


class Parser(object):
    def parse(self, help_root_dir):
        if not os.path.isdir(help_root_dir):
            raise HelpGeneratorError(
                'HGE_NO_EXISTING_DIRECTORY',
                f'"{help_root_dir}" is not an existing directory')
        file_parser = HelpFileParser()
        parser = HelpNodeParser(file_parser)
        root = parser.parse(help_root_dir)

        return root
