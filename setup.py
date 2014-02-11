#!/usr/bin/env python

from setuptools import setup, find_packages
from atlastools import pkginfo
from glob import glob

setup(
    name='atlastools',
    version=pkginfo.__RELEASE__,
    description='ATLAS utilities',
    author='Noel Dawe',
    author_email='noel.dawe@cern.ch',
    url='http://github.com/ndawe/atlastools',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
        'configobj',
        'goodruns'],
    zip_safe=False,
    scripts=glob('scripts/*') + ['atlastools/etc/grid-setup.sh'],
    package_data={'': ['etc/*']},)
