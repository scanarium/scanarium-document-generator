import os


class DocumentNodeParser(object):
    def __init__(self, file_parser):
        self.file_parser = file_parser

    def parse(self, dir):
        files = {}
        subnodes = []

        for file in sorted(os.listdir(dir)):
            file_full = os.path.join(dir, file)
            if os.path.isdir(file_full):
                subnodes.append(self.parse(file_full))
            else:
                file = self.file_parser.parse(file_full)
                files[file['key']] = file

        ret = {
            'name': dir,
            'files': files,
            'subnodes': subnodes,
            }

        return ret
