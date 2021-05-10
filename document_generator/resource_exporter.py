import os
import shutil


class ResourceExporter(object):
    def __init__(self, resources, output_dir):
        self.resources = resources
        self.output_dir = output_dir

    def export(self):
        for source in self.resources:
            dest = os.path.join(self.output_dir, os.path.basename(source))
            shutil.copytree(source, dest, dirs_exist_ok=True)
