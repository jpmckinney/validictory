#!/usr/bin/env python

from setuptools import setup, find_packages

from validictory import __version__
DESCRIPTION = "general purpose python data validator"
LONG_DESCRIPTION = open('README.rst').read()

setup(name='validictory',
      version=__version__,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author='James Turk',
      author_email='jturk@sunlightfoundation.com',
      url='http://github.com/sunlightlabs/validictory',
      license="MIT License",
      platforms=["any"],
      packages=find_packages(),
      test_suite="validictory.tests",
     )
