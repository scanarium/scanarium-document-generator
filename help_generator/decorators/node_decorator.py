from .decorator import Decorator


class NodeDecorator(Decorator):
    def decorate_node(self, file, state):
        pass

    def decorate_node_enter(self, node, state):
        self.decorate_node(node, state)
