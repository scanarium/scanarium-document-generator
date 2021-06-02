import copy

from .decorator import Decorator
from .utils import Utils


class PropertyDecorator(Decorator):
    def __init__(self, initial_state={}):
        self.utils = Utils()
        self.initial_state = initial_state

    def init_state(self, node):
        state = super().init_state(node)

        # The `ancestor-properties` list keeps track of the properties of each
        # parent of the current node we traverse the hierarchy. The current
        # node's properties are at the end of the list.
        #
        # Preparing initial properties to act as ancestor properties
        # for root node.
        state['ancestor-properties'] = [
            {'properties': copy.deepcopy(self.initial_state)}]
        return state

    def decorate_node_enter(self, node, state):
        properties = {}
        if 'properties' in node['files']:
            properties = node['files']['properties']['content-properties']

        state['ancestor-properties'].append({'properties': properties})

    def decorate_file(self, file, state):
        # The `properties` file got covered in `decorate_node_enter` already,
        # so we skip over it.
        if file['key'] != 'properties':
            current_level = state['ancestor-properties'][-1]
            key = file['key'] if 'is-default' not in file else 'default'
            current_level[key] = file['content-properties']

            properties = {}
            for level_properties in state['ancestor-properties']:
                if 'properties' in level_properties:
                    self.utils.update_dict(
                        properties,
                        copy.deepcopy(level_properties['properties']))
                if file['key'] in level_properties:
                    self.utils.update_dict(
                        properties,
                        copy.deepcopy(level_properties[file['key']]))
                elif 'default' in level_properties:
                    self.utils.update_dict(
                        properties, copy.deepcopy(level_properties['default']))

            properties['language'] = file['key']

            file['properties'] = properties

    def decorate_node_exit(self, node, state):
        # Removing our own state again. So the end of the list holds our
        # ancestors' state again.
        del state['ancestor-properties'][-1]
