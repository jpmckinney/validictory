import re
import sys
import copy
import socket
from datetime import datetime
from decimal import Decimal
from collections import Mapping, Container
import itertools

if sys.version_info[0] == 3:
    _str_type = str
    _int_types = (int,)
else:
    _str_type = basestring
    _int_types = (int, long)


class SchemaError(ValueError):
    """
    errors encountered in processing a schema (subclass of :class:`ValueError`)
    """


class ValidationError(ValueError):
    """
    validation errors encountered during validation (subclass of
    :class:`ValueError`)
    """


class FieldValidationError(ValidationError):
    """
    validation error that refers to a specific field
    Includes `fieldname` and `value` attributes.
    """
    def __init__(self, message, fieldname, value):
        super(FieldValidationError, self).__init__(message)
        self.fieldname = fieldname
        self.value = value


def _generate_datetime_validator(format_option, dateformat_string):
    def validate_format_datetime(validator, fieldname, value, format_option):
        try:
            datetime.strptime(value, dateformat_string)
        except ValueError:
            yield FieldValidationError(
                "Value %(value)r of field '%(fieldname)s' is not in "
                "'%(format_option)s' format" % locals(), fieldname, value)

    return validate_format_datetime

validate_format_date_time = _generate_datetime_validator('date-time',
                                                         '%Y-%m-%dT%H:%M:%SZ')
validate_format_date = _generate_datetime_validator('date', '%Y-%m-%d')
validate_format_time = _generate_datetime_validator('time', '%H:%M:%S')


def validate_format_utc_millisec(validator, fieldname, value, format_option):
    if not isinstance(value, _int_types + (float, Decimal)):
        yield FieldValidationError("Value %(value)r of field '%(fieldname)s' "
                                   "is not a number" % locals(), fieldname,
                                   value)

    if not value > 0:
        yield FieldValidationError("Value %(value)r of field '%(fieldname)s' "
                                   " is not a positive number" % locals(),
                                   fieldname, value)


def validate_format_ip_address(validator, fieldname, value, format_option):
    try:
        socket.inet_aton(value)
        # Make sure we expect "X.X.X.X" as socket.inet_aton() converts "1"
        # to "0.0.0.1"
        ip = len(value.split('.')) == 4
    except:
        ip = False
    if not ip:
        yield FieldValidationError("Value %(value)r of field '%(fieldname)s'"
                                   "is not a ip-address" % locals(), fieldname,
                                   value)


DEFAULT_FORMAT_VALIDATORS = {
    'date-time': validate_format_date_time,
    'date': validate_format_date,
    'time': validate_format_time,
    'utc-millisec': validate_format_utc_millisec,
    'ip-address': validate_format_ip_address,
}


class SchemaValidator(object):
    '''
    Validator largely based upon the JSON Schema proposal but useful for
    validating arbitrary python data structures.

    :param format_validators: optional dictionary of custom format validators
    :param required_by_default: defaults to True, set to False to make
        ``required`` schema attribute False by default.
    :param blank_by_default: defaults to False, set to True to make ``blank``
        schema attribute True by default.
    :param disallow_unknown_properties: defaults to False, set to True to
        disallow properties not listed in the schema definition
    '''

    def __init__(self, format_validators=None, required_by_default=True,
                 blank_by_default=False, disallow_unknown_properties=False):
        if format_validators is None:
            format_validators = DEFAULT_FORMAT_VALIDATORS.copy()

        self._format_validators = format_validators
        self.required_by_default = required_by_default
        self.blank_by_default = blank_by_default
        self.disallow_unknown_properties = disallow_unknown_properties

    def register_format_validator(self, format_name, format_validator_fun):
        self._format_validators[format_name] = format_validator_fun

    def validate_type_string(self, val):
        return isinstance(val, _str_type)

    def validate_type_integer(self, val):
        return type(val) in _int_types

    def validate_type_number(self, val):
        return type(val) in _int_types + (float, Decimal,)

    def validate_type_boolean(self, val):
        return type(val) == bool

    def validate_type_object(self, val):
        return isinstance(val, Mapping) or (hasattr(val, 'keys')
                                            and hasattr(val, 'items'))

    def validate_type_array(self, val):
        return isinstance(val, (list, tuple))

    def validate_type_null(self, val):
        return val is None

    def validate_type_any(self, val):
        return True

    def _error(self, desc, value, fieldname, **params):
        params['value'] = value
        params['fieldname'] = fieldname
        message = desc % params
        return FieldValidationError(message, fieldname, value)

    def _validate_unknown_properties(self, schema, data, fieldname):
        schema_properties = set(schema)
        data_properties = set(data)
        delta = data_properties - schema_properties
        if delta:
            unknowns = ''
            for x in delta:
                unknowns += '"%s", ' % x
            unknowns = unknowns.rstrip(", ")
            raise SchemaError('Unknown properties for field '
                              '"%(fieldname)s": %(unknowns)s' %
                              locals())

    def validate_type(self, x, fieldname, schema, fieldtype=None):
        '''
        Validates that the fieldtype specified is correct for the given
        data
        '''

        # We need to know if the field exists or if it's just Null
        fieldexists = True
        try:
            value = x[fieldname]
        except KeyError:
            fieldexists = False
            value = None

        if fieldtype and fieldexists:
            if isinstance(fieldtype, (list, tuple)):
                # Match if type matches any one of the types in the list
                datavalid = False
                errors = iter([])
                for eachtype in fieldtype:
                    more_errors = list(self.validate_type(x, fieldname, eachtype, eachtype))
                    datavalid |= len(more_errors) == 0
                    errors = itertools.chain(errors, iter(more_errors))
                if not datavalid:
                    yield self._error("Value %(value)r for field '%(fieldname)s' "
                                "doesn't match any of %(numsubtypes)d "
                                "subtypes in %(fieldtype)s; "
                                "errorlist = %(errors)r",
                                value, fieldname, numsubtypes=len(fieldtype),
                                fieldtype=fieldtype, errorlist=errors)
            elif isinstance(fieldtype, dict):
                for e in self.__validate(fieldname, x, fieldtype):
                    yield e
            else:
                try:
                    type_checker = getattr(self, 'validate_type_%s' %
                                           fieldtype)
                except AttributeError:
                    raise SchemaError("Field type '%s' is not supported." %
                                      fieldtype)

                if not type_checker(value):
                    yield self._error("Value %(value)r for field '%(fieldname)s' "
                                "is not of type %(fieldtype)s",
                                value, fieldname, fieldtype=fieldtype)

    def validate_properties(self, x, fieldname, schema, properties=None):
        '''
        Validates properties of a JSON object by processing the object's
        schema recursively
        '''
        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if isinstance(value, dict):
                if isinstance(properties, dict):

                    if self.disallow_unknown_properties:
                        self._validate_unknown_properties(properties, value,
                                                          fieldname)

                    for eachProp in properties:
                        for e in self.__validate(eachProp, value, properties.get(eachProp)):
                            yield e
                else:
                    raise SchemaError("Properties definition of field '%s' is "
                                      "not an object" % fieldname)

    def validate_items(self, x, fieldname, schema, items=None):
        '''
        Validates that all items in the list for the given field match the
        given schema
        '''
        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if isinstance(value, (list, tuple)):
                if isinstance(items, (list, tuple)):
                    if (not 'additionalItems' in schema and
                            len(items) != len(value)):
                        yield self._error("Length of list %(value)r for field "
                                    "'%(fieldname)s' is not equal to length "
                                    "of schema list", value, fieldname)
                    else:
                        for itemIndex in range(len(items)):
                            for e in self.validate(value[itemIndex], items[itemIndex]):
                                yield type(e)(
                                              "Failed to validate field '%s' "
                                              "list schema: %s" %
                                              (fieldname, e), fieldname,
                                              e.value)
                elif isinstance(items, dict):
                    for eachItem in value:
                        if (self.disallow_unknown_properties and
                                'properties' in items):
                            self._validate_unknown_properties(
                                items['properties'], eachItem, fieldname)

                        for e in self._validate(eachItem, items):
                            # a bit of a hack: replace reference to _data
                            # with 'list item' so error messages make sense
                            old_error = str(e).replace("field '_data'",
                                                       'list item')
                            yield type(e)("Failed to validate field '%s' list "
                                          "schema: %s" %
                                          (fieldname, old_error), fieldname,
                                          e.value)
                else:
                    raise SchemaError("Properties definition of field '%s' is "
                                      "not a list or an object" % fieldname)

    def validate_required(self, x, fieldname, schema, required):
        '''
        Validates that the given field is present if required is True
        '''
        # Make sure the field is present
        if fieldname not in x and required:
            yield self._error("Required field '%(fieldname)s' is missing",
                        None, fieldname)

    def validate_blank(self, x, fieldname, schema, blank=False):
        '''
        Validates that the given field is not blank if blank=False
        '''
        value = x.get(fieldname)
        if isinstance(value, _str_type) and not blank and not value:
            yield self._error("Value %(value)r for field '%(fieldname)s' cannot be "
                        "blank'", value, fieldname)

    def validate_patternProperties(self, x, fieldname, schema,
                                   patternproperties=None):

        if patternproperties is None:
            patternproperties = {}

        value_obj = x.get(fieldname, {})

        for pattern, schema in patternproperties.items():
            for key, value in value_obj.items():
                if re.match(pattern, key):
                    self.validate(value, schema)

    def validate_additionalItems(self, x, fieldname, schema,
                                 additionalItems=False):
        value = x.get(fieldname)

        if not isinstance(value, (list, tuple)):
            return

        if isinstance(additionalItems, bool):
            if additionalItems or 'items' not in schema:
                return
            elif len(value) != len(schema['items']):
                yield self._error("Length of list %(value)r for field "
                            "'%(fieldname)s' is not equal to length of schema "
                            "list", value, fieldname)

        remaining = value[len(schema['items']):]
        if len(remaining) > 0:
            self._validate(remaining, {'items': additionalItems})

    def validate_additionalProperties(self, x, fieldname, schema,
                                      additionalProperties=None):
        '''
        Validates additional properties of a JSON object that were not
        specifically defined by the properties property
        '''

        # Shouldn't be validating additionalProperties on non-dicts
        value = x.get(fieldname)
        if not isinstance(value, dict):
            return

        # If additionalProperties is the boolean value True then we accept
        # any additional properties.
        if isinstance(additionalProperties, bool) and additionalProperties:
            return

        value = x.get(fieldname)
        if isinstance(additionalProperties, (dict, bool)):
            properties = schema.get("properties")
            if properties is None:
                properties = {}
            if value is None:
                value = {}
            for eachProperty in value:
                if eachProperty not in properties:
                    # If additionalProperties is the boolean value False
                    # then we don't accept any additional properties.
                    if (isinstance(additionalProperties, bool) and not
                            additionalProperties):
                        yield self._error("additional property '%(prop)s' "
                                    "not defined by 'properties' are not "
                                    "allowed in field '%(fieldname)s'",
                                    None, fieldname, prop=eachProperty)
                    self.__validate(eachProperty, value,
                                    additionalProperties)
        else:
            raise SchemaError("additionalProperties schema definition for "
                              "field '%s' is not an object" % fieldname)

    def validate_dependencies(self, x, fieldname, schema, dependencies=None):
        if x.get(fieldname) is not None:

            # handle cases where dependencies is a string or list of strings
            if isinstance(dependencies, _str_type):
                dependencies = [dependencies]
            if isinstance(dependencies, (list, tuple)):
                for dependency in dependencies:
                    if dependency not in x:
                        yield self._error("Field '%(dependency)s' is required by "
                                    "field '%(fieldname)s'",
                                    None, fieldname, dependency=dependency)
            elif isinstance(dependencies, dict):
                # NOTE: the version 3 spec is really unclear on what this means
                # based on the meta-schema I'm assuming that it should check
                # that if a key exists, the appropriate value exists
                for k, v in dependencies.items():
                    if k in x and v not in x:
                        yield self._error("Field '%(v)s' is required by field "
                                    "'%(k)s'", None, fieldname, k=k, v=v)
            else:
                raise SchemaError("'dependencies' must be a string, "
                                  "list of strings, or dict")

    def validate_minimum(self, x, fieldname, schema, minimum=None):
        '''
        Validates that the field is longer than or equal to the minimum
        length if specified
        '''

        exclusive = schema.get('exclusiveMinimum', False)

        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if value is not None:
                if (type(value) in (int, float) and
                    (not exclusive and value < minimum) or
                        (exclusive and value <= minimum)):
                    yield self._error("Value %(value)r for field '%(fieldname)s' is "
                                "less than minimum value: %(minimum)f",
                                value, fieldname, minimum=minimum)

    def validate_maximum(self, x, fieldname, schema, maximum=None):
        '''
        Validates that the field is shorter than or equal to the maximum
        length if specified.
        '''

        exclusive = schema.get('exclusiveMaximum', False)

        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if value is not None:
                if (type(value) in (int, float) and
                    (not exclusive and value > maximum) or
                        (exclusive and value >= maximum)):
                    yield self._error("Value %(value)r for field '%(fieldname)s' is "
                                "greater than maximum value: %(maximum)f",
                                value, fieldname, maximum=maximum)

    def validate_maxLength(self, x, fieldname, schema, length=None):
        '''
        Validates that the value of the given field is shorter than or equal
        to the specified length
        '''
        value = x.get(fieldname)
        if isinstance(value, (_str_type, list, tuple)) and len(value) > length:
            yield self._error("Length of value %(value)r for field '%(fieldname)s' "
                        "must be less than or equal to %(length)d",
                        value, fieldname, length=length)

    def validate_minLength(self, x, fieldname, schema, length=None):
        '''
        Validates that the value of the given field is longer than or equal
        to the specified length
        '''
        value = x.get(fieldname)
        if isinstance(value, (_str_type, list, tuple)) and len(value) < length:
            yield self._error("Length of value %(value)r for field '%(fieldname)s' "
                        "must be greater than or equal to %(length)d",
                        value, fieldname, length=length)

    validate_minItems = validate_minLength
    validate_maxItems = validate_maxLength

    def validate_format(self, x, fieldname, schema, format_option=None):
        '''
        Validates the format of primitive data types
        '''
        value = x.get(fieldname)

        format_validator = self._format_validators.get(format_option, None)

        if format_validator and value:
            return format_validator(self, fieldname, value, format_option)
        return iter([])

        # TODO: warn about unsupported format ?

    def validate_pattern(self, x, fieldname, schema, pattern=None):
        '''
        Validates that the given field, if a string, matches the given
        regular expression.
        '''
        value = x.get(fieldname)
        if isinstance(value, _str_type):
            if not re.match(pattern, value):
                yield self._error("Value %(value)r for field '%(fieldname)s' does "
                            "not match regular expression '%(pattern)s'",
                            value, fieldname, pattern=pattern)

    def validate_uniqueItems(self, x, fieldname, schema, uniqueItems=False):
        '''
        Validates that all items in an array instance MUST be unique
        (contains no two identical values).
        '''

        # If additionalProperties is the boolean value True then we accept
        # any additional properties.
        if isinstance(uniqueItems, bool) and not uniqueItems:
            return

        values = x.get(fieldname)

        if not isinstance(values, (list, tuple)):
            return

        hashables = set()
        unhashables = []

        for value in values:
            if isinstance(value, (list, dict)):
                container, add = unhashables, unhashables.append
            else:
                container, add = hashables, hashables.add

            if value in container:
                yield self._error(
                    "Value %(value)r for field '%(fieldname)s' is not unique",
                    value, fieldname)
            else:
                add(value)

    def validate_enum(self, x, fieldname, schema, options=None):
        '''
        Validates that the value of the field is equal to one of the
        specified option values
        '''
        value = x.get(fieldname)
        if value is not None:
            if not isinstance(options, Container):
                raise SchemaError("Enumeration %r for field '%s' must be a "
                                  "container", (options, fieldname))
            if value not in options:
                yield self._error("Value %(value)r for field '%(fieldname)s' is not "
                            "in the enumeration: %(options)r",
                            value, fieldname, options=options)

    def validate_title(self, x, fieldname, schema, title=None):
        if not isinstance(title, (_str_type, type(None))):
            raise SchemaError("The title for field '%s' must be a string" %
                              fieldname)

    def validate_description(self, x, fieldname, schema, description=None):
        if not isinstance(description, (_str_type, type(None))):
            raise SchemaError("The description for field '%s' must be a string"
                              % fieldname)

    def validate_divisibleBy(self, x, fieldname, schema, divisibleBy=None):
        value = x.get(fieldname)

        if not self.validate_type_number(value):
            return

        if divisibleBy == 0:
            raise SchemaError("'%r' <- divisibleBy can not be 0" % schema)

        if value % divisibleBy != 0:
            yield self._error("Value %(value)r field '%(fieldname)s' is not "
                        "divisible by '%(divisibleBy)s'.",
                        x.get(fieldname), fieldname, divisibleBy=divisibleBy)

    def validate_disallow(self, x, fieldname, schema, disallow=None):
        '''
        Validates that the value of the given field does not match the
        disallowed type.
        '''
        if len(self.validate_type(x, fieldname, schema, disallow)) == 0:
            return
        yield self._error("Value %(value)r of type %(disallow)s is disallowed for "
                    "field '%(fieldname)s'",
                    x.get(fieldname), fieldname, disallow=disallow)

    def validate(self, data, schema):
        '''
        Validates a piece of json data against the provided json-schema.
        '''
        return self._validate(data, schema)

    def _validate(self, data, schema):
        return self.__validate("_data", {"_data": data}, schema)

    def __validate(self, fieldname, data, schema):

    	errors = iter([])  

        if schema is not None:
            if not isinstance(schema, dict):
                raise SchemaError(
                    "Type for field '%s' must be 'dict', got: '%s'" %
                    (fieldname, type(schema).__name__))

            newschema = copy.copy(schema)

            if 'optional' in schema:
                raise SchemaError('The "optional" attribute has been replaced'
                                  ' by "required"')
            if 'requires' in schema:
                raise SchemaError('The "requires" attribute has been replaced'
                                  ' by "dependencies"')

            if 'required' not in schema:
                newschema['required'] = self.required_by_default
            if 'blank' not in schema:
                newschema['blank'] = self.blank_by_default

            for schemaprop in newschema:

                validatorname = "validate_" + schemaprop

                validator = getattr(self, validatorname, None)
                if validator:
                    errors = itertools.chain(
                        errors,
                        validator(data, fieldname, schema, newschema.get(schemaprop)))

        return errors

__all__ = ['SchemaValidator', 'FieldValidationError']
