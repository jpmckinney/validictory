#!/usr/bin/env python

from validictory.validator import SchemaValidator, ValidationError

__all__ = [ 'validate', 'SchemaValidator', 'ValidationError' ]
__version__ = '0.6.1'

def validate(data, schema, validator_cls=SchemaValidator,
             format_validators=None, required_by_default=True):
    '''
    Validates a parsed json document against the provided schema. If an
    error is found a ValueError is raised.

    ``data`` is a python dictionary object of parsed json data.

    ``schema`` is a python dictionary object representing the schema.

    If ``validator_cls`` is provided that class will be used to validate
    the given ``schema`` against the given ``data``. The given class should
    be a subclass of the SchemaValidator class.

    If ``format_validators`` is provided, the validator_cls will be
    instanciated with these default format validators.

    ``required_by_default`` specifies if ``required`` should default to True
    or False (default: True)
    '''
    v = validator_cls(format_validators, required_by_default)
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
