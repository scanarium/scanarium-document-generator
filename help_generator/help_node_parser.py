import os


class HelpNodeParser(object):
    def __init__(self, file_parser):
        self.file_parser = file_parser

    def parse(self, dir):
        files = []
        subnodes = []

        for file in sorted(os.listdir(dir)):
            file_full = os.path.join(dir, file)
            if os.path.isdir(file_full):
                subnodes.append(self.parse(file_full))
            else:
                files.append(self.file_parser.parse(file_full))

        ret = {
            'files': files,
            'subnodes': subnodes,
            }

        return ret
