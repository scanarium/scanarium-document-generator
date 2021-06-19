import os
import shutil


class ResourceExporter(object):
    def __init__(self, resources, output_dir):
        self.resources = resources
        self.output_dir = output_dir

    def export_resource(self, source):
        if source.endswith('*'):
            resource_dir = os.path.dirname(source)
            for resource_file in os.listdir(resource_dir):
                self.export_resource(os.path.join(resource_dir, resource_file))
        else:
            if os.path.isdir(source):
                dest = os.path.join(self.output_dir, os.path.basename(source))
                shutil.copytree(source, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(source, self.output_dir)

    def export(self):
        for source in self.resources:
            self.export_resource(source)
