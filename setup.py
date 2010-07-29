#!/usr/bin/env python
#:coding=utf-8:

from ez_setup import use_setuptools
import sys
if 'cygwin' in sys.platform.lower():
   min_version='0.6c6'
else:
   min_version='0.6a9'
try:
    use_setuptools(min_version=min_version)
except TypeError:
    # If a non-local ez_setup is already imported, it won't be able to
    # use the min_version kwarg and will bail with TypeError
    use_setuptools()

if sys.version < '2.3':
    sys.exit('Error: Python-2.3 or newer is required. Current version:\n %s' % sys.version)

from setuptools import setup, find_packages

VERSION = "0.3"
DESCRIPTION = "json-schema validator for Python"
LONG_DESCRIPTION = """
jsonschema is a complete, full featured validator for json-schema
adhering to the json-schema proposal second draft.
<http://groups.google.com/group/json-schema/web/json-schema-proposal---second-draft>.

jsonschema is written in pure python and currently has no dependencies.

Validators may be subclassed much like simplejson encoders to provide
special functionality or extensions.

jsonschema currently supports ascii and utf-8 json and schema documents.
"""

CLASSIFIERS = filter(None, map(str.strip,
"""
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
""".splitlines()))

setup(name='jsonschema',
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author='James Turk',
      author_email='james.p.turk@gmail.com',
      url='http://github.com/jamesturk/jsonschema',
      license="MIT License",
      platforms=["any"],
      packages=find_packages(exclude=['ez_setup']),
      test_suite="jsonschema.tests",
      zip_safe=False
     )
