from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    readme = f.read()


setup(
    name='ansible_importer',
    version='0.0.2',
    description='Small library to allow Ansible plugins/modules to be imported.',
    long_description=readme,
    license='GPLv3',
    url='https://github.com/nrb/ansible_importer',
    author='Nolan Brubaker',
    author_email='palendae@gmail.com',
    package_data={'': ['LICENSE']},
    packages=find_packages(),
    py_modules=[
        'ansible_importer',
    ],
    include_package_data=True,
    zip_safe=True,
    classifiers=(
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',

    )
)
