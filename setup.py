#!/usr/bin/env python

from atlastools import pkginfo
from distutils.core import setup
from glob import glob

setup(name='atlastools',
      version=pkginfo.__RELEASE__,
      description='ATLAS utilities',
      author='Noel Dawe',
      author_email='noel.dawe@cern.ch',
      url='http://noel.mine.nu/repo',
      packages=['atlastools'],
      requires=['rootpy', 'yaml', 'goodruns'],
      scripts=glob('scripts/*'),
      data_files = [('dat', glob('dat/*'))]
     )

