import collections.abc
import subprocess


class Utils(object):
    def update_dict(self, target, source, merge_lists=False):
        for key, value in source.items():
            if isinstance(value, collections.abc.Mapping):
                repl = self.update_dict(target.get(key, {}), value)
                target[key] = repl
            elif merge_lists and isinstance(value, list) \
                    and isinstance(target.get(key, 0), list):
                target[key] += value
            else:
                target[key] = source[key]
        return target

    def extract_title(self, markdown):
        markdown_lines = markdown.split('\n')
        title = ''

        while not title and markdown_lines:
            title = markdown_lines[0].strip()
            del markdown_lines[0]

        if title:
            while title.startswith('#'):
                title = title[1:].strip()

        if title:
            title = title.split('{:', 1)[0].strip()

        return title

    def run_command(self, command):
        process = subprocess.run(command,
                                 check=True,
                                 timeout=3,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        return {
            'stdout': process.stdout,
            'stderr': process.stderr,
        }
