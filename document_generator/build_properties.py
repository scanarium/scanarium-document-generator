import datetime
import os

from .decorators import Utils

GIT = '/usr/bin/git'


class BuildProperties(object):
    def __init__(self, markdown_dir):
        self.markdown_dir = markdown_dir
        self.utils = Utils()

    def addTimeFields(self, d):
        now = datetime.datetime.now(datetime.timezone.utc)
        d['build_seconds_since_epoch'] = str(now.timestamp())
        d['build_day_iso'] = now.strftime('%Y-%m-%d')

    def addGitFields(self, d):
        dir = os.path.abspath(self.markdown_dir)
        last_dir = ''
        git_dir = None
        while not git_dir and dir != last_dir:
            git_dir = os.path.join(dir, '.git')
            if not os.path.isdir(git_dir):
                git_dir = None
                dir = os.path.dirname(dir)

        description = 'no-description-found'
        try:
            result = self.utils.run_command([
                    GIT,
                    '--git-dir', git_dir,
                    'describe',
                    '--always',
                    '--dirty=/d'])
            description = result['stdout'].split('\n')[0]
        except Exception:
            pass

        d['build_git_description'] = description

    def getProperties(self):
        ret = {}

        self.addTimeFields(ret)
        self.addGitFields(ret)

        return ret
