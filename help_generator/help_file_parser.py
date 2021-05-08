class HelpFileParser(object):
    def parse(self, file_name):
        ret = {
            'file_name': file_name
            }

        with open(file_name, 'rt') as f:
            raw_content = f.read()

        ret['markdown'] = raw_content
        return ret
