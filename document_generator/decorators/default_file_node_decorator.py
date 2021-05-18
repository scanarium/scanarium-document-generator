import copy

from .node_decorator import NodeDecorator


class DefaultFileNodeDecorator(NodeDecorator):
    def __init__(self, default_l10n):
        self.default_l10n = default_l10n

    def decorate_node(self, node, state):
        files = node['files']
        if files:
            # Since we want to avoid interference of default language and the
            # 'default' file, we cannot simply assign, but have to deepcopy.
            files['default'] = copy.deepcopy(files[self.default_l10n])
            files['default']['is-default'] = True
