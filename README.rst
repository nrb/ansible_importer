ansible_importer
----------------

Ansible modules and plugins are typically pure Python, but often lack the structure necessary to import 
as Python code. This package is meant to allow programmers to import module code for testing purposes.

Installing
----------

The code's up on PyPI

.. code-block:: bash

    pip install ansible_importer

Usage
-----

.. code-block:: python

    import ansible_importer
    ansible_importer.install('/abs/path/to/ansible/code')

    # Assuming above path has a playbooks/plugins/actions/my_plugin.py module
    from playbooks.plugins.actions.my_plugin import ActionModule

    # Assuming playbooks/library/glance
    from playbooks.library.glance import ManageGlance

    # Assuming playbooks/inventory/dynamic_inventory.py
    from playbooks.inventory import dynamic_inventory

Credits
-------

Thanks to Raphael Randschau for the idea of using the `imp module`, and Doug Hellman's Python Module of the Week post on `import hooks` for guidance in implementation.


.. _`imp module`: https://nicolai86.eu/blog/posts/2014-02-05/testing-ansible-libraries/
.. _`import hooks`: https://pymotw.com/2/sys/imports.html
