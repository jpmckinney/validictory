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
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.6",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   ("Topic :: Software Development :: Libraries :: "
                    "Python Modules"),
                   ],
     )
