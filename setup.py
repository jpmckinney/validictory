#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = "0.4"
DESCRIPTION = "general purpose validator for data in python dictionaries"
LONG_DESCRIPTION = open('README.rst').read()

CLASSIFIERS = filter(None, map(str.strip,
"""
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
""".splitlines()))

setup(name='validictory',
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author='James Turk',
      author_email='james.p.turk@gmail.com',
      url='http://github.com/sunlightlabs/validictory',
      license="MIT License",
      platforms=["any"],
      packages=find_packages(),
      test_suite="validictory.tests",
     )
