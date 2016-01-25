import imp
import os
import sys

PLAYBOOK_ROOT = 'playbooks'

INVENTORY_DIR = 'inventory'

LIBRARY_DIR = 'library'

PLUGIN_DIR = 'plugins'

PLUGINS = [
    'actions',
    'callbacks',
    'filters',
    'lookups',
]

ANSIBLE_DIRS = ['playbooks', 'inventory', 'library', 'plugins']


class AnsibleModuleImporter(object):

    def __init__(self, path):
        print("Received path {}".format(path))
        # Make sure that what we act on is really inside on an ansible project.
        contents = os.listdir(path)
        ansible_dirs = set(ANSIBLE_DIRS).intersection(contents)
        plugin_dirs = set(PLUGINS).intersection(contents)

        if not ansible_dirs and not plugin_dirs:
            raise ImportError()

        self._path = path

    def find_module(self, fullname, path=None):
        """
        Finds a module called 'fullname' at filesystem 'path'.

        The 'fullname' received will be a dotted path, and we'll receive one per segement,
        e.g.
            playbooks
            playbooks.plugins
            playbooks.plugins.actions
        """
        print("Received fullname {}".format(fullname))

        parts = fullname.split('.')

        # Only operate on the most recent part of the dotted name
        basename = parts[-1]

        self.path = os.path.join(self._path, basename)

        if not os.path.exists(self.path) and not os.path.exists(self.path + '.py'):
            print("Path doesn't exist")
            return None

        self._parts = parts
        self.basename = basename
        self.extension = ''

        # When importing plugins, we'll need the extension.
        # Modules generally don't need that.
        if os.path.exists(self.path + '.py'):
            self.extension = '.py'

        print("Successfully returning")
        return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        mod = imp.new_module(self.basename)
        mod.__loader__ = self

        # We don't want to actually load unless we get to the Python code.
        print("Trying to load {}".format(fullname))
        if self.basename not in ANSIBLE_DIRS and self.basename not in PLUGINS:
            mod = imp.load_source(self.basename, self.path + self.extension)
        mod.__file__ = "[placeholder for {}]".format(fullname)
        mod.__path__ = [self.path]
        mod.__package__ = self.basename
        sys.modules[self.basename] = mod
        return mod


def install(root_path):
    sys.path_hooks.append(AnsibleModuleImporter)
    sys.path.append(root_path)
