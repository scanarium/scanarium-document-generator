import os

from .document_generator_error import DocumentGeneratorError
from .document_file_parser import DocumentFileParser
from .document_node_parser import DocumentNodeParser


class Parser(object):
    def parse(self, document_root_dir):
        if not os.path.isdir(document_root_dir):
            raise DocumentGeneratorError(
                'HGE_NO_EXISTING_DIRECTORY',
                f'"{document_root_dir}" is not an existing directory')
        file_parser = DocumentFileParser()
        parser = DocumentNodeParser(file_parser)
        root = parser.parse(document_root_dir)

        return root
