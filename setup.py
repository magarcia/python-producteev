#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import producteev

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

if sys.argv[1] == 'docs':
    try:
        import sphinx
    except ImportError:
        sys.stderr.write('You must be install sphinx for make docs.\n')
        sys.stderr.write('\t pip install sphinx\n')
        sys.exit(-1)

    build_command = 'make html'
    if len(sys.argv) >= 3:
        if sys.argv[2].lower() == 'latex':
            build_command = 'make latex'
        elif sys.argv[2].lower() == 'pdf':
            build_command = 'make latexpdf'
        elif sys.argv[2].lower() == 'html':
            build_command = 'make html'
        else:
            sys.stderr.write('Unrecognized format.\n')
            sys.exit(-1)

    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    os.chdir(docs_dir)
    os.system(build_command)
    os.chdir(os.path.pardir)
    sys.exit()

required = []


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        return "This is a Python wrapper for the Producteev API."


setup(
    name='producteev',
    version=producteev.__version__,
    description='Producteev API.',
    author='Martín García',
    author_email='newluxfero@gmail.com',
    long_description = read('README.rst'),
    url='https://github.com/magarcia/python-producteev',
    packages=['producteev'],
    package_data={'': ['LICENSE',]},
    include_package_data=True,
    install_requires=required,
    license='MIT',
    test_suite='tests',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3.0',
        # 'Programming Language :: Python :: 3.1',
    ),
)