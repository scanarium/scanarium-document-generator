import copy

from .decorator import Decorator
from .utils import Utils


class PropertyDecorator(Decorator):
    def __init__(self, initial_state={}):
        self.utils = Utils()
        self.initial_state = initial_state

    def init_state(self):
        state = super().init_state()

        # The `properties-list` list acts as storage for states as we traverse
        # the hierarchy. The current node's properties are at the end of the
        # list.
        #
        # Preparing initial properties to act as parent properties
        # for root node.
        state['properties-list'] = [copy.deepcopy(self.initial_state)]
        return state

    def decorate_node_enter(self, node, state):
        # Seeding from properties of parent node.
        properties = copy.deepcopy(state['properties-list'][-1])

        if node['files']:
            # Overriding with `default` file's properties
            self.utils.update_dict(properties, copy.deepcopy(
                    node['files']['default']['content-properties']))

            # Overriding with `property` file's properties
            if 'properties' in node['files']:
                self.utils.update_dict(properties, copy.deepcopy(
                        node['files']['properties']['content-properties']))

        # Appending our own state, so file decorations can find the current
        # state at the end of the list.
        state['properties-list'].append(properties)

    def decorate_file(self, file, state):
        properties = copy.deepcopy(state['properties-list'][-1])
        self.utils.update_dict(
            properties, copy.deepcopy(file['content-properties']))
        properties['language'] = file['key']
        file['properties'] = properties

    def decorate_node_exit(self, node, state):
        # Removing our own state again. So the end of the list holds our
        # parent's state again.
        del state['properties-list'][-1]
