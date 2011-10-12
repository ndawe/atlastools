#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from atlastools import pkginfo
from setuptools import setup
from glob import glob

setup(name='atlastools',
      version=pkginfo.__RELEASE__,
      description='ATLAS utilities',
      author='Noel Dawe',
      author_email='noel.dawe@cern.ch',
      url='http://noel.mine.nu/repo',
      packages=['atlastools'],
      requires=['rootpy', 'yaml', 'goodruns'],
      zip_safe=False,
      scripts=glob('scripts/*'),
      package_data={'': ['etc/*']}
     )
