#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from atlastools import pkginfo
from setuptools import setup, find_packages
from glob import glob

from distutils.core import Extension

jet_cleaning = Extension('atlastools/jets/_libcleaning',
                    sources = ['atlastools/jets/_libcleaning.cpp',
                               'atlastools/jets/_cleaning.cpp'])

setup(name='atlastools',
      version=pkginfo.__RELEASE__,
      description='ATLAS utilities',
      author='Noel Dawe',
      author_email='noel.dawe@cern.ch',
      url='http://github.com/ndawe/atlastools',
      packages=find_packages(),
      install_requires=['PyYAML', 'configobj', 'goodruns', 'argparse'],
      zip_safe=False,
      scripts=glob('scripts/*') + ['atlastools/etc/grid-setup.sh'],
      package_data={'': ['etc/*']},
      ext_modules = [jet_cleaning]
     )
