#!/usr/bin/env python

from validictory.validator import (SchemaValidator, FieldValidationError, MultipleValidationError,
                                   ValidationError, SchemaError)

__all__ = ['validate', 'SchemaValidator', 'FieldValidationError', 'MultipleValidationError',
           'ValidationError', 'SchemaError']
__version__ = '1.1.0'


def validate(data, schema, validator_cls=SchemaValidator,
             format_validators=None, required_by_default=True,
             blank_by_default=False, disallow_unknown_properties=False,
             apply_default_to_data=False, fail_fast=True,
             remove_unknown_properties=False):
    '''
    Validates a parsed json document against the provided schema. If an
    error is found a :class:`ValidationError` is raised.

    If there is an issue in the schema a :class:`SchemaError` will be raised.

    :param data:  python data to validate
    :param schema: python dictionary representing the schema (see
        `schema format`_)
    :param validator_cls: optional validator class (default is
        :class:`SchemaValidator`)
    :param format_validators: optional dictionary of custom format validators
    :param required_by_default: defaults to True, set to False to make
        ``required`` schema attribute False by default.
    :param disallow_unknown_properties: defaults to False, set to True to
        disallow properties not listed in the schema definition
    :param apply_default_to_data: defaults to False, set to True to modify the
        data in case the schema definition includes a "default" property
    :param fail_fast: defaults to True, set to False if you prefer to get
        all validation errors back instead of only the first one
    :param remove_unknown_properties: defaults to False, set to True to
        filter out properties not listed in the schema definition. Only applies
        when disallow_unknown_properties is False.
    '''
    v = validator_cls(format_validators, required_by_default, blank_by_default,
                      disallow_unknown_properties, apply_default_to_data, fail_fast,
                      remove_unknown_properties)
    return v.validate(data, schema)

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
    except ValueError as e:
        raise SystemExit(e)
