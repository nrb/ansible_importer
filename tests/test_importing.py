import os

import unittest

import ansible_importer
path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# This is super gross - doing the install means we've mutated global state.


class TestImporting(unittest.TestCase):
    def setUp(self):
        ansible_importer.install(path)

    def cleanUp(self):
        ansible_importer.uninstall(path)

    def testImportingLibrary(self):
        from playbooks.library.test_lib import target
        self.assertEqual('test_lib/target imported', target())

    def testImportingActionPlugin(self):
        from playbooks.plugins.actions.my_action import an_action
        self.assertEqual('ran an action', an_action())

    def testImportingLookupPlugin(self):
        from playbooks.plugins.lookups.my_lookup import a_lookup
        self.assertEqual('ran a lookup', a_lookup())

    def testImportingCallbackPlugin(self):
        from playbooks.plugins.callbacks.my_callback import a_callback
        self.assertEqual('ran a callback', a_callback())

    def testImportingFilterPlugin(self):
        from playbooks.plugins.filters.my_filter import a_filter
        self.assertEqual('ran a filter', a_filter())

    def testImportingInventory(self):
        from playbooks.inventory.dyn_inv import inventory
        self.assertEqual('made an inventory', inventory())


if __name__ == '__main__':
    unittest.main()
