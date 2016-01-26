from setuptools import setup, find_packages

setup(
    name='ansible_importer',
    version='0.0.1',
    description='Small library to allow Ansible plugins/modules to be imported.',
    author='Nolan Brubaker',
    author_email='palendae@gmail.com',
    packages=find_packages(),
    py_modules=[
        'ansible_importer',
    ],
    include_package_data=True,
    zip_safe=True,
)
