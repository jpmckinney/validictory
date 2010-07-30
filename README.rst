===========
validictory
===========

A general purpose python data validator.

Schema format based on JSON Schema Proposal (http://json-schema.org)

Contains code derived from jsonschema, by Ian Lewis and Yusuke Muraoka.

Usage
=====

JSON documents and schema must first be loaded into a python dictionary type
before it can be validated.

Parsing a simple JSON document::

    >>> import jsonschema
    >>> jsonschema.validate("simplejson", {"type":"string"})

    Parsing a more complex JSON document::

    >>> import simplejson
    >>> import jsonschema
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
    >>> jsonschema.validate(data,schema)

Handling validation errors
ValueErrors are thrown when validation errors occur.::

    >>> import jsonschema
    >>> try:
    ...     jsonschema.validate("simplejson", {"type":"string","minLength":15})
    ... except ValueError, e:
    ...     print e.message
    ...
    Length of 'simplejson' must be more than 15.000000
