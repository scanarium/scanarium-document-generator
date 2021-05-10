import os

from .document_generator_error import DocumentGeneratorError
from .markdown_renderer import MarkdownRenderer

HEADER = '<html><meta>' \
    '<meta http-equiv="Content-type" content="text/html;charset=UTF-8" />' \
    '</meta><body>'
FOOTER = '</body></html>'


class AllInOneExporter(object):
    def __init__(self, root_node, output_dir, default_l10n, other_l10ns,
                 conf={}):
        self.root_node = root_node
        self.output_dir = output_dir
        self.default_l10n = default_l10n
        self.all_l10ns = [self.default_l10n] + other_l10ns
        self.header = HEADER
        self.footer = FOOTER

        if 'html-template-file' in conf:
            with open(conf['html-template-file'], 'rt') as f:
                header_lines = []
                footer_lines = []
                mode = 'HEADER'
                for line in f.readlines():
                    if mode == 'HEADER':
                        if line.strip() == '<!-- HEADER-END -->':
                            mode = 'MIDDLE'
                        else:
                            header_lines.append(line)
                    elif mode == 'MIDDLE':
                        if line.strip() == '<!-- FOOTER-START -->':
                            mode = 'FOOTER'
                    elif mode == 'FOOTER':
                        footer_lines.append(line)
                    else:
                        raise DocumentGeneratorError(
                            'SE_LOGIC', f'Unknown mode "{mode}"')

                self.header = '\n'.join(header_lines)
                self.footer = '\n'.join(footer_lines)

        if 'html-header-file' in conf:
            with open(conf['html-header-file'], 'rt') as f:
                self.header = f.read()

        if 'html-footer-file' in conf:
            with open(conf['html-footer-file'], 'rt') as f:
                self.footer = f.read()

    def _get_full_markdown(self, node, l10n):
        ret = ''

        files = node['files']
        if files:
            try:
                file = files[l10n]
            except KeyError:
                try:
                    file = files[self.default_l10n]
                except KeyError:
                    raise DocumentGeneratorError(
                        'HGE_MISSING_L10N',
                        f'No localization "{l10n}" missing for node '
                        f'{node["name"]} and default "{self.default_l10n}" '
                        f'does not exist either')

            ret = file['markdown']

        for subnode in node['subnodes']:
            ret += '\n\n' + self._get_full_markdown(subnode, l10n)

        return ret

    def export(self):
        renderer = MarkdownRenderer()
        for l10n in self.all_l10ns:
            markdown = self._get_full_markdown(self.root_node, l10n)
            file = os.path.join(self.output_dir, f'all.html.{l10n}')
            with open(file, 'w+') as f:
                f.write(self.header)
                f.write(renderer.render(markdown))
                f.write(self.footer)
