import sys

import unittest


class TestImportInstaller(unittest.TestCase):
    def testInstallingAndUninstalling(self):
        import ansible_importer
        ansible_importer.install('playbooks')
        self.assertEqual('playbooks', sys.path[-1])
        self.assertEqual(ansible_importer.AnsibleModuleImporter,
                         sys.path_hooks[-1])

        ansible_importer.uninstall('playbooks')
        self.assertFalse('playbooks' in sys.path)
        self.assertFalse(ansible_importer.AnsibleModuleImporter in sys.path_hooks)

if __name__ == '__main__':
    unittest.main()
