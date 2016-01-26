import imp
import os
import sys


# Some common lists we'll need to know about.
PLUGINS = [
    'actions',
    'callbacks',
    'filters',
    'lookups',
]

ANSIBLE_DIRS = ['playbooks', 'inventory', 'library', 'plugins']

# A list that holds the paths that have been activated for our importer.
_VALID_PATHS = []

class AnsibleModuleImporter(object):

    def __init__(self, given_path):

        # If the path we're given doesn't fall in our valid paths, bail
        if not any([p in given_path for p in _VALID_PATHS]):
            raise ImportError()

        self._path = given_path

    def find_module(self, fullname, path=None):
        """
        Finds a module called 'fullname' at filesystem 'path'.

        The 'fullname' received will be a dotted path, and we'll receive one
        per segement, e.g.
            playbooks
            playbooks.plugins
            playbooks.plugins.actions
        """

        parts = fullname.split('.')

        # Only operate on the most recent part of the dotted name
        basename = parts[-1]

        # Hold on to the filesystem path for when we do a load.
        self.path = os.path.join(self._path, basename)

        # If the directory structure/files don't exist, leave.
        if not any([os.path.exists(self.path + e) for e in ('', '.py')]):
            return None

        self._parts = parts
        self.basename = basename
        self.extension = ''

        # When importing plugins, we'll need the extension.
        # Modules generally don't need it, though.
        if os.path.exists(self.path + '.py'):
            self.extension = '.py'

        return self

    def load_module(self, fullname):
        """
        Loads the source for a module found at `fullname`.

        For most of the module path here, we're going to be generating
        placeholders that don't actually have code; they'd be the equivalent of
        a bunch of empty dirs with __init__.py's, but ansible doesn't have the
        init file in the path.
        """
        if fullname in sys.modules:
            mod = sys.modules[fullname]
        else:
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))

        mod.__file__ = os.path.join(self.path, fullname)
        mod.__loader__ = self
        mod.__path__ = [self.path]
        mod.__package__ = '.'.join(fullname.split('.')[:-1])

        # We don't want to actually load unless we get to the Python code.
        # This is assuming that the guards in the __init__() function worked
        if self.basename not in ANSIBLE_DIRS and self.basename not in PLUGINS:
            mod = imp.load_source(self.basename, self.path + self.extension)
        return mod


def install(root_path):
    """
    Installs the module importer, valid only for the specified root path.

    This must be called explicitly so that the library isn't doing anything
    behind the caller's back. The actual importer class will only look in the
    provided `root_path`, so that it's not stomping on other python imports.

    Use this before you want to import an Ansible module.
    """
    # TODO: Make this more robust so we don't install multiple copies of
    # the importer
    sys.path_hooks.append(AnsibleModuleImporter)
    sys.path.append(root_path)
    _VALID_PATHS.append(root_path)

def uninstall(root_path):
    """
    Remove importer from hooks and remove specified paths
    """
    try:
        _VALID_PATHS.remove(root_path)
    except ValueError:
        pass

    try:
        sys.path.remove(root_path)
    except ValueError:
        pass

    try:
        sys.path_hooks.remove(AnsibleModuleImporter)
    except ValueError:
        pass
