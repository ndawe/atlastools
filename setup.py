#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from atlastools import pkginfo
from setuptools import setup, find_packages
from glob import glob

setup(name='atlastools',
      version=pkginfo.__RELEASE__,
      description='ATLAS utilities',
      author='Noel Dawe',
      author_email='noel.dawe@cern.ch',
      url='http://github.com/ndawe/atlastools',
      packages=find_packages(),
      install_requires=['rootpy', 'PyYAML', 'configobj', 'goodruns', 'argparse'],
      zip_safe=False,
      scripts=glob('scripts/*') + ['atlastools/etc/grid-setup.sh'],
      package_data={'': ['etc/*']}
     )
