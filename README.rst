===========
validictory
===========

:warning: **:warning: As of 2018 this library is deprecated, please consider using jsonschema (https://pypi.python.org/pypi/jsonschema) instead.**


.. image:: https://travis-ci.org/jamesturk/validictory.svg?branch=master
    :target: https://travis-ci.org/jamesturk/validictory

.. image:: https://coveralls.io/repos/jamesturk/validictory/badge.png?branch=master
    :target: https://coveralls.io/r/jamesturk/validictory

.. image:: https://img.shields.io/pypi/v/validictory.svg
    :target: https://pypi.python.org/pypi/validictory

.. image:: https://readthedocs.org/projects/validictory/badge/?version=latest
    :target: https://readthedocs.org/projects/validictory/?badge=latest
    :alt: Documentation Status


A general purpose Python data validator.

Schema format based on JSON Schema Proposal (http://json-schema.org)

Contains code derived from jsonschema, by Ian Lewis and Yusuke Muraoka.

Usage
=====

JSON documents and schema must first be loaded into a Python dictionary type
before it can be validated.

Parsing a simple JSON document::

    >>> import validictory
    >>>
    >>> validictory.validate("something", {"type":"string"})

Parsing a more complex JSON document::

    >>> import json
    >>> import validictory
    >>>
    >>> data = json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
    >>> schema = {
    ...   "type":"array",
    ...   "items":[
    ...     {"type":"string"},
    ...     {"type":"object",
    ...      "properties":{
    ...        "bar":{
    ...          "items":[
    ...            {"type":"string"},
    ...            {"type":"any"},
    ...            {"type":"number"},
    ...            {"type":"integer"}
    ...          ]
    ...        }
    ...      }
    ...    }
    ...   ]
    ... }
    >>> validictory.validate(data,schema)

Catch ValueErrors to handle validation issues::

    >>> import validictory
    >>>
    >>> try:
    ...     validictory.validate("something", {"type":"string","minLength":15})
    ... except ValueError, error:
    ...     print(error)
    ...
    Length of value 'something' for field '_data' must be greater than or equal to 15

You can read more in the official documentation at `Read the Docs <http://validictory.readthedocs.org/en/latest/>`_.
