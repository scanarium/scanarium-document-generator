import os


class DocumentFileParser(object):
    def parse(self, file_name):
        key = os.path.basename(file_name)
        if key.endswith('.md'):
            key = key[:-3]
        ret = {
            'key': key,
            'file_name': file_name
            }

        with open(file_name, 'rt') as f:
            raw_content = f.read()

        ret['markdown'] = raw_content
        return ret
