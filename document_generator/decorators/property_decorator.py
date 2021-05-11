import copy

from .decorator import Decorator
from .utils import Utils


class PropertyDecorator(Decorator):
    def __init__(self):
        self.utils = Utils()

    def decorate_node_enter(self, node, state):
        if node['files']:
            state['properties'] = copy.deepcopy(
                node['files']['default']['content-properties'])
            if 'properties' in node['files']:
                self.utils.update_dict(
                    state['properties'],
                    node['files']['properties']['content-properties'])

    def decorate_file(self, file, state):
        properties = copy.deepcopy(state['properties'])
        self.utils.update_dict(
            properties, copy.deepcopy(file['content-properties']))
        properties['language'] = file['key']
        file['properties'] = properties
