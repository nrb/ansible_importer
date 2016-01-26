# ansible_importer

Ansible modules and plugins are typically pure Python, but often lack the structure necessary to import 
as Python code. This package is meant to allow programmers to import module code for testing purposes.

# Usage

```
    import ansible_importer
    ansible_importer.install('/abs/path/to/ansible/code')

    from playbooks.plugins.actions.my_plugin import ActionModule
```

