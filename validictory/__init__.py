#!/usr/bin/env python

'''
A general purpose validator for data in python dictionaries.

Schema format based on JSON Schema Proposal (http://json-schema.org)

Contains code derived from jsonschema, by Ian Lewis and Yusuke Muraoka.

Parsing a simple JSON document

>>> import validictory
>>> validictory.validate("simplejson", {"type":"string"})

Parsing a more complex JSON document.

>>> import simplejson
>>> import validictory
>>>
>>> data = simplejson.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
>>> schema = {
...     "type":"array",
...     "items":[
...         {"type":"string"},
...         {"type":"object",
...            "properties":{
...                "bar":{
...                    "items":[
...                        {"type":"string"},
...                        {"type":"any"},
...                        {"type":"number"},
...                        {"type":"integer"}
...                    ]
...                }
...            }
...        }
...     ]
... }
>>> validictory.validate(data,schema)

Handling validation errors
ValueErrors are thrown when validation errors occur.

>>> import validictory
>>> try:
...         validictory.validate("simplejson",
...                                 {"type":"string","minLength":15})
... except ValueError, e:
...         print str(e)
...
Length of value 'simplejson' for field '_data' must be more than or equal to 15.000000

Running from the command line

% echo '{"type":"string"}' > schema.json
% echo '"mystring"' | python -mvalidictory schema.json

% echo '"mystring"' > data.json
% python -mvalidictory schema.json data.json

'''

from validictory.validator import SchemaValidator

__all__ = [ 'validate', 'SchemaValidator' ]
__version__ = '0.4'

def validate(data, schema, validator_cls=SchemaValidator):
    '''
    Validates a parsed json document against the provided schema. If an
    error is found a ValueError is raised.

    ``data`` is a python dictionary object of parsed json data.

    ``schema`` is a python dictionary object representing the schema.

    If ``validator_cls`` is provided that class will be used to validate
    the given ``schema`` against the given ``data``. The given class should
    be a subclass of the SchemaValidator class.
    '''
    v = validator_cls()
    return v.validate(data,schema)

if __name__ == '__main__':
    import sys
    import json
    if len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            raise SystemExit("%s SCHEMAFILE [INFILE]" % (sys.argv[0],))
        schemafile = open(sys.argv[1], 'rb')
        infile = sys.stdin
    elif len(sys.argv) == 3:
        schemafile = open(sys.argv[1], 'rb')
        infile = open(sys.argv[2], 'rb')
    else:
        raise SystemExit("%s SCHEMAFILE [INFILE]" % (sys.argv[0],))
    try:
        obj = json.load(infile)
        schema = json.load(schemafile)
        validate(obj, schema)
    except ValueError, e:
        raise SystemExit(e)
