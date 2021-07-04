import os

from .document_generator_error import DocumentGeneratorError
from .markdown_renderer import MarkdownRenderer
from .decorators import Utils
from .decorators import ValueInjectorFileDecorator

HEADER = '<html><meta>' \
    '<meta http-equiv="Content-type" content="text/html;charset=UTF-8" />' \
    '</meta><body>'
FOOTER = '</body></html>'


class AllInOneExporter(object):
    def __init__(self, root_node, output_dir, default_l10n, other_l10ns,
                 conf={}, value_injector=None, value_injector_state=None):
        self.root_node = root_node
        self.output_dir = output_dir
        self.default_l10n = default_l10n
        self.all_l10ns = [self.default_l10n] + other_l10ns
        self.header = HEADER
        self.footer = FOOTER
        self.value_injector = value_injector
        self.value_injector_state = value_injector_state
        self.utils = Utils()
        self.value_injector = ValueInjectorFileDecorator()
        self.value_injector_state = self.value_injector.init_state(root_node)

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
        id = None
        markdown = ''
        title = '(anonymous)'
        sort_key = ''

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

            try:
                id = file['properties']['id']
            except KeyError:
                # There's no id here. Since we're not enforcing ids, we prod on
                # without it.
                pass
            markdown = file['markdown']

            title = self.utils.extract_title(markdown)

            sort_key = file['properties'].get('sort-key', sort_key).strip()

        if not sort_key:
            sort_key = '{node-dir-name}'
        sort_key = sort_key.replace('{node-dir-name}',
                                    os.path.basename(node['name']).lower())
        sort_key = sort_key.replace('{title}', title.lower())

        capsules = []
        for subnode in node['subnodes']:
            capsules.append(self._get_full_markdown(subnode, l10n))

        capsules.sort(key=lambda e: e['sort_key'])

        def linkedToc(file, state, args):
            ret = '\n'
            for capsule in capsules:
                capsule_id = capsule["id"]
                ret += '\n* '
                if capsule_id:
                    ret += f'[{capsule["title"]}](#{capsule_id})'
                else:
                    ret += capsule["title"]
            ret += '\n\n'
            return ret

        markdown = self.value_injector.decorate_text(
            markdown, self.value_injector_state, funcs={
                'linkedToc': linkedToc,
                })

        for capsule in capsules:
            markdown += '\n\n' + capsule['markdown']

        return {
            'id': id,
            'sort_key': sort_key,
            'title': title,
            'markdown': markdown
            }

    def inject_values(self, text, l10n, properties):
        ret = text
        if self.value_injector:
            ret = self.value_injector.decorate_text(
                ret, self.value_injector_state, key=l10n,
                properties=properties)
        return ret

    def export(self):
        renderer = MarkdownRenderer()
        for l10n in self.all_l10ns:
            properties = self.root_node['files'].get(
                l10n, self.root_node['files']['default'])['properties']
            header = self.inject_values(self.header, l10n, properties)
            footer = self.inject_values(self.footer, l10n, properties)

            capsule = self._get_full_markdown(self.root_node, l10n)
            markdown = capsule['markdown']

            file = os.path.join(self.output_dir, f'all.html.{l10n}')
            with open(file, 'w+') as f:
                f.write(header)
                f.write(renderer.render(markdown))
                f.write(footer)

            file = os.path.join(self.output_dir, f'all.md.{l10n}')
            with open(file, 'w+') as f:
                f.write(markdown)
