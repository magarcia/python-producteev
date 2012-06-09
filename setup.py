#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import producteev

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
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