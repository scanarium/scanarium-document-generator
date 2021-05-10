class Decorator(object):
    def init_state(self):
        return {}

    def decorate_file(self, file, state):
        pass

    def decorate_node_enter(self, node, state):
        pass

    def decorate_node_exit(self, node, state):
        pass

    def run(self, node, state={}):
        self.decorate_node_enter(node, state)

        for file_key in sorted(node['files'].keys()):
            self.decorate_file(node['files'][file_key], state)

        for subnode in node['subnodes']:
            self.run(subnode, state)

        self.decorate_node_exit(node, state)
