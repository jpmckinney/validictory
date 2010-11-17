===========
validictory
===========

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
    >>> validictory.validate("simplejson", {"type":"string"})

Parsing a more complex JSON document::

    >>> import simplejson
    >>> import validictory
    >>>
    >>> data = simplejson.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
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
    ...     validictory.validate("simplejson", {"type":"string","minLength":15})
    ... except ValueError, error:
    ...     print error
    ...
    Length of value 'simplejson' for field '_data' must be greater than or equal to 15
