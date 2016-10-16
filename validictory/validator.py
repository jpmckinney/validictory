import re
import sys
import copy
import socket
from datetime import datetime
from decimal import Decimal
from collections import Mapping, Container

if sys.version_info[0] == 3:
    _str_type = str
    _int_types = (int,)
else:
    _str_type = basestring
    _int_types = (int, long)


class SchemaError(ValueError):
    """ errors encountered in processing a schema (subclass of :class:`ValueError`) """


class ValidationError(ValueError):
    """ validation errors encountered during validation (subclass of :class:`ValueError`) """


class FieldValidationError(ValidationError):
    """
    Validation error that refers to a specific field and has `fieldname` and `value` attributes.
    """
    def __init__(self, message, fieldname, value, path=''):
        message = "Value {0!r} for field '{1}' {2}".format(value, path, message)
        super(FieldValidationError, self).__init__(message)
        self.fieldname = fieldname
        self.value = value
        self.path = path


class DependencyValidationError(ValidationError):
    """
    Validation error that refers to a missing dependency
    """
    def __init__(self, message):
        super(DependencyValidationError, self).__init__(message)


class RequiredFieldValidationError(ValidationError):
    """
    Validation error that refers to a missing field
    """
    def __init__(self, message):
        super(RequiredFieldValidationError, self).__init__(message)


class MultipleValidationError(ValidationError):
    def __init__(self, errors):
        msg = "{0} validation errors:\n{1}".format(len(errors), '\n'.join(str(e) for e in errors))
        super(MultipleValidationError, self).__init__(msg)
        self.errors = errors


def _generate_datetime_validator(format_option, dateformat_string):
    def validate_format_datetime(validator, fieldname, value, format_option):
        try:
            # Additions to support date-time with microseconds without breaking
            # existing date-time validation.
            # Microseconds will appear specifically separated by a period, as
            # some variable length decimal number
            # such as  '2015-11-18T19:57:05.061Z' instead of
            # '2015-11-18T19:57:05Z'  Better would be to use
            # strict_rfc3339 vs datetime.strptime though the user needs the
            #  package installed for the import to succeed.
            #     import strict_rfc3339
            #     assert strict_rfc3339.validate_rfc3339(value)
            if format_option == 'date-time' and '.' in value:
                datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
            else:
                datetime.strptime(value, dateformat_string)
        except:
            msg = "is not in '{format_option}' format"
            raise FieldValidationError(msg.format(format_option=format_option), fieldname, value)

    return validate_format_datetime

validate_format_date_time = _generate_datetime_validator('date-time', '%Y-%m-%dT%H:%M:%SZ')
validate_format_date = _generate_datetime_validator('date', '%Y-%m-%d')
validate_format_time = _generate_datetime_validator('time', '%H:%M:%S')


def validate_format_utc_millisec(validator, fieldname, value, format_option):
    if not isinstance(value, _int_types + (float, Decimal)) or value <= 0:
        msg = "is not a positive number"
        raise FieldValidationError(msg, fieldname, value)


def validate_format_ip_address(validator, fieldname, value, format_option):
    try:
        # Make sure we expect "X.X.X.X" as socket.inet_aton() converts "1" to "0.0.0.1"
        socket.inet_aton(value)
        ip = len(value.split('.')) == 4
    except:
        ip = False
    if not ip:
        msg = "is not a ip-address"
        raise FieldValidationError(msg, fieldname, value)


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
    :param apply_default_to_data: defaults to False, set to True to modify the
        data in case the schema definition includes a "default" property
    :param fail_fast: defaults to True, set to False if you prefer to get
        all validation errors back instead of only the first one
    :param remove_unknown_properties: defaults to False, set to True to
        filter out properties not listed in the schema definition. Only applies
        when disallow_unknown_properties is False.
    '''

    def __init__(self, format_validators=None, required_by_default=True,
                 blank_by_default=False, disallow_unknown_properties=False,
                 apply_default_to_data=False, fail_fast=True,
                 remove_unknown_properties=False):

        self._format_validators = {}
        self._errors = []

        # add the default format validators
        for key, value in DEFAULT_FORMAT_VALIDATORS.items():
            self.register_format_validator(key, value)

        # register any custom format validators if they were provided
        if format_validators:
            for key, value in format_validators.items():
                self.register_format_validator(key, value)
        self.required_by_default = required_by_default
        self.blank_by_default = blank_by_default
        self.disallow_unknown_properties = disallow_unknown_properties
        self.apply_default_to_data = apply_default_to_data
        self.fail_fast = fail_fast

        # disallow_unknown_properties takes precedence over remove_unknown_properties
        self.remove_unknown_properties = remove_unknown_properties

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
        return isinstance(val, Mapping) or (hasattr(val, 'keys') and hasattr(val, 'items'))

    def validate_type_array(self, val):
        return isinstance(val, (list, tuple))

    def validate_type_null(self, val):
        return val is None

    def validate_type_any(self, val):
        return True

    def _error(self, desc, value, fieldname, exctype=FieldValidationError, path='', **params):
        params['value'] = value
        params['fieldname'] = fieldname
        message = desc.format(**params)

        if exctype == FieldValidationError:
            err = FieldValidationError(message, fieldname, value, path)
        elif exctype == DependencyValidationError or exctype == RequiredFieldValidationError:
            err = exctype(message)
            err.fieldname = fieldname
            err.path = path

        if self.fail_fast:
            raise err
        else:
            self._errors.append(err)

    def _validate_unknown_properties(self, schema, data, fieldname, patternProperties):
        """Raise a SchemaError when unknown fields are found."""
        schema_properties = set(schema)
        data_properties = set(data)
        delta = data_properties - schema_properties
        if self.disallow_unknown_properties and delta:
            unknowns = ', '.join(['"{0}"'.format(x) for x in delta])
            raise SchemaError('Unknown properties for field "{fieldname}": {unknowns}'.format(
                fieldname=fieldname, unknowns=unknowns))

        elif self.remove_unknown_properties:
            patterns = patternProperties.keys() if patternProperties else []

            if patterns:
                delta = [f for f in delta if not any(re.match(p, f) for p in patterns)]

            for unknown_field in delta:
                del data[unknown_field]

    def validate_type(self, x, fieldname, schema, path, fieldtype=None):
        ''' Validates that the fieldtype specified is correct for the given data '''

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
                errorlist = []
                for eachtype in fieldtype:
                    try:
                        # if fail_fast is False, _error will not rais an exception.
                        # need to monitor the _errors list as well
                        errors = self._errors[:]
                        self.validate_type(x, fieldname, eachtype, path, eachtype)
                        if len(self._errors) > len(errors):
                            # an exception was raised.
                            # remove the error from self.errors and raise it here
                            raise self._errors.pop()

                        datavalid = True
                        break
                    except (SchemaError, ValidationError) as err:
                        errorlist.append(err)
                if not datavalid:
                    self._error("doesn't match any of {numsubtypes} subtypes in {fieldtype}; "
                                "errorlist = {errorlist!r}",
                                value, fieldname, path=path, numsubtypes=len(fieldtype),
                                fieldtype=fieldtype, errorlist=errorlist)
            elif isinstance(fieldtype, dict):
                try:
                    self.__validate(fieldname, x, fieldtype, path)
                except ValueError as e:
                    raise e
            else:
                try:
                    type_checker = getattr(self, 'validate_type_' + fieldtype)
                except AttributeError:
                    raise SchemaError("Field type '{0}' is not supported.".format(fieldtype))

                if not type_checker(value):
                    self._error("is not of type {fieldtype}", value, fieldname, path=path,
                                fieldtype=fieldtype)

    def validate_properties(self, x, fieldname, schema, path, properties=None):
        ''' Validates properties of a JSON object by processing the object's schema recursively '''
        value = x.get(fieldname)
        if value is not None:
            if isinstance(value, dict):
                if isinstance(properties, dict):

                    if self.disallow_unknown_properties or self.remove_unknown_properties:
                        self._validate_unknown_properties(properties, value, fieldname,
                                                          schema.get('patternProperties'))

                    for property in properties:
                        self.__validate(property, value, properties.get(property),
                                        path + '.' + property)
                else:
                    raise SchemaError("Properties definition of field '{0}' is not an object"
                                      .format(fieldname))

    def validate_items(self, x, fieldname, schema, path, items=None):
        '''
        Validates that all items in the list for the given field match the given schema
        '''
        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if isinstance(value, (list, tuple)):
                if isinstance(items, (list, tuple)):
                    if 'additionalItems' not in schema and len(items) != len(value):
                        self._error("is not of same length as schema list", value, fieldname,
                                    path=path)
                    else:
                        for index, item in enumerate(items):
                            try:
                                self.__validate("_data", {"_data": value[index]}, item,
                                                '{0}[{1}]'.format(path, index))
                            except FieldValidationError as e:
                                raise type(e)("Failed to validate field '%s' list schema: %s" %
                                              (fieldname, e), fieldname, e.value)
                elif isinstance(items, dict):
                    for index, item in enumerate(value):
                        if ((self.disallow_unknown_properties or
                             self.remove_unknown_properties) and 'properties' in items):
                            self._validate_unknown_properties(items['properties'],
                                                              item,
                                                              fieldname,
                                                              schema.get('patternProperties'))

                        self.__validate("[list item]", {"[list item]": item}, items,
                                        '{0}[{1}]'.format(path, index))
                else:
                    raise SchemaError("Properties definition of field '{0}' is "
                                      "not a list or an object".format(fieldname))

    def validate_required(self, x, fieldname, schema, path, required):
        ''' Validates that the given field is present if required is True '''
        # Make sure the field is present
        if fieldname not in x and required:
            self._error("Required field '{fieldname}' is missing", None, fieldname, path=path,
                        exctype=RequiredFieldValidationError)

    def validate_blank(self, x, fieldname, schema, path, blank=False):
        ''' Validates that the given field is not blank if blank=False '''
        value = x.get(fieldname)
        if isinstance(value, _str_type) and not blank and not value:
            self._error("cannot be blank'", value, fieldname, path=path)

    def validate_patternProperties(self, x, fieldname, schema, path, patternproperties=None):

        if patternproperties is None:
            patternproperties = {}

        value_obj = x.get(fieldname, {})

        for pattern, schema in patternproperties.items():
            for key, value in value_obj.items():
                if re.match(pattern, key):
                    self.__validate("_data", {"_data": value}, schema, path)

    def validate_additionalItems(self, x, fieldname, schema, path, additionalItems=False):
        value = x.get(fieldname)

        if not isinstance(value, (list, tuple)):
            return

        if isinstance(additionalItems, bool):
            if additionalItems or 'items' not in schema:
                return
            elif len(value) != len(schema['items']):
                self._error("is not of same length as schema list", value, fieldname, path=path)

        remaining = value[len(schema['items']):]
        if len(remaining) > 0:
            self.__validate("_data", {"_data": remaining}, {"items": additionalItems}, path)

    def validate_additionalProperties(self, x, fieldname, schema, path, additionalProperties=None):
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
            patterns = schema["patternProperties"].keys() if 'patternProperties' in schema else []
            if properties is None:
                properties = {}
            if value is None:
                value = {}
            for eachProperty in value:
                if (eachProperty not in properties and not
                        any(re.match(p, eachProperty) for p in patterns)):
                    # If additionalProperties is the boolean value False
                    # then we don't accept any additional properties.
                    if additionalProperties is False:
                        self._error("contains additional property '{prop}' not defined by "
                                    "'properties' or 'patternProperties' and additionalProperties "
                                    " is False", value, fieldname, prop=eachProperty, path=path)
                    self.__validate(eachProperty, value, additionalProperties, path)
        else:
            raise SchemaError("additionalProperties schema definition for "
                              "field '{0}' is not an object".format(fieldname))

    def validate_dependencies(self, x, fieldname, schema, path, dependencies=None):
        if x.get(fieldname) is not None:

            # handle cases where dependencies is a string or list of strings
            if isinstance(dependencies, _str_type):
                dependencies = [dependencies]
            if isinstance(dependencies, (list, tuple)):
                for dependency in dependencies:
                    if dependency not in x:
                        self._error("Field '{dependency}' is required by field '{fieldname}'",
                                    None, fieldname, dependency=dependency, path=path,
                                    exctype=DependencyValidationError)
            elif isinstance(dependencies, dict):
                # NOTE: the version 3 spec is really unclear on what this means
                # based on the meta-schema I'm assuming that it should check
                # that if a key exists, the appropriate value exists
                for k, v in dependencies.items():
                    if k in x and v not in x:
                        self._error("Field '{k}' is required by field '{v}'", None, fieldname,
                                    k=k, v=v, exctype=DependencyValidationError, path=path)
            else:
                raise SchemaError("'dependencies' must be a string, list of strings, or dict")

    def validate_minimum(self, x, fieldname, schema, path, minimum=None):
        ''' Validates that the field is longer than or equal to the minimum length if specified '''

        exclusive = schema.get('exclusiveMinimum', False)

        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if value is not None:
                if (type(value) in (int, float) and
                    (not exclusive and value < minimum) or
                        (exclusive and value <= minimum)):
                    self._error("is less than minimum value: {minimum}", value, fieldname,
                                minimum=minimum, path=path)

    def validate_maximum(self, x, fieldname, schema, path, maximum=None):
        '''
        Validates that the field is shorter than or equal to the maximum length if specified.
        '''

        exclusive = schema.get('exclusiveMaximum', False)

        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if value is not None:
                if (type(value) in (int, float) and
                    (not exclusive and value > maximum) or
                        (exclusive and value >= maximum)):
                    self._error("is greater than maximum value: {maximum}", value, fieldname,
                                maximum=maximum, path=path)

    def validate_maxProperties(self, x, fieldname, schema, path, number=None):
        '''
        Validates that the number of properties of the given object is less than or equal
        to the specified number
        '''
        value = x.get(fieldname)
        if isinstance(value, dict) and len(value) > number:
            self._error("must have number of properties less than or equal to {number}",
                        value, fieldname, number=number, path=path)

    def validate_minProperties(self, x, fieldname, schema, path, number=None):
        '''
        Validates that the number of properties of the given object is greater than or equal
        to the specified number
        '''
        value = x.get(fieldname)
        if isinstance(value, dict) and len(value) < number:
            self._error("must have number of properties greater than or equal to {number}",
                        value, fieldname, number=number, path=path)

    def validate_maxLength(self, x, fieldname, schema, path, length=None):
        '''
        Validates that the value of the given field is shorter than or equal
        to the specified length
        '''
        value = x.get(fieldname)
        if isinstance(value, (_str_type, list, tuple)) and len(value) > length:
            self._error("must have length less than or equal to {length}", value, fieldname,
                        length=length, path=path)

    def validate_minLength(self, x, fieldname, schema, path, length=None):
        '''
        Validates that the value of the given field is longer than or equal to the specified length
        '''
        value = x.get(fieldname)
        if isinstance(value, (_str_type, list, tuple)) and len(value) < length:
            self._error("must have length greater than or equal to {length}", value, fieldname,
                        length=length, path=path)

    validate_minItems = validate_minLength
    validate_maxItems = validate_maxLength

    def validate_format(self, x, fieldname, schema, path, format_option=None):
        '''
        Validates the format of primitive data types
        '''
        value = x.get(fieldname, None)

        format_validator = self._format_validators.get(format_option, None)

        if format_validator and value is not None:
            try:
                format_validator(self, fieldname, value, format_option)
            except FieldValidationError as fve:
                if self.fail_fast:
                    raise
                else:
                    self._errors.append(fve)

        # TODO: warn about unsupported format ?

    def validate_pattern(self, x, fieldname, schema, path, pattern=None):
        '''
        Validates that the given field, if a string, matches the given regular expression.
        '''
        value = x.get(fieldname)
        if (isinstance(value, _str_type) and
            (isinstance(pattern, _str_type) and not re.match(pattern, value)
             or not isinstance(pattern, _str_type) and not pattern.match(value))):
            self._error("does not match regular expression '{pattern}'", value, fieldname,
                        pattern=pattern, path=path)

    def validate_uniqueItems(self, x, fieldname, schema, path, uniqueItems=False):
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
                self._error("is not unique", value, fieldname, path=path)
            else:
                add(value)

    def validate_enum(self, x, fieldname, schema, path, options=None):
        '''
        Validates that the value of the field is equal to one of the specified option values
        '''
        value = x.get(fieldname)
        if value is not None:
            if callable(options):
                options = options(x)
            if not isinstance(options, Container):
                raise SchemaError("Enumeration {0!r} for field '{1}' must be a container".format(
                                  options, fieldname))
            if value not in options:
                if not(value == '' and schema.get('blank', self.blank_by_default)):
                    self._error("is not in the enumeration: {options!r}", value, fieldname,
                                options=options, path=path)

    def validate_title(self, x, fieldname, schema, path, title=None):
        if not isinstance(title, (_str_type, type(None))):
            raise SchemaError("The title for field '{0}' must be a string".format(fieldname))

    def validate_description(self, x, fieldname, schema, path, description=None):
        if not isinstance(description, (_str_type, type(None))):
            raise SchemaError("The description for field '{0}' must be a string".format(fieldname))

    def validate_divisibleBy(self, x, fieldname, schema, path, divisibleBy=None):
        value = x.get(fieldname)

        if not self.validate_type_number(value):
            return

        if divisibleBy == 0:
            raise SchemaError("'{0!r}' <- divisibleBy can not be 0".format(schema))

        if value % divisibleBy != 0:
            self._error("is not divisible by '{divisibleBy}'.", x.get(fieldname), fieldname,
                        divisibleBy=divisibleBy, path=path)

    def validate_disallow(self, x, fieldname, schema, path, disallow=None):
        '''
        Validates that the value of the given field does not match the disallowed type.
        '''
        try:
            self.validate_type(x, fieldname, schema, path, disallow)
        except ValidationError:
            return
        self._error("is disallowed for field '{fieldname}'", x.get(fieldname), fieldname,
                    disallow=disallow, path=path)

    def validate(self, data, schema):
        '''
        Validates a piece of json data against the provided json-schema.
        '''
        self.__validate("data", {"data": data}, schema, '<obj>')
        if self._errors:
            raise MultipleValidationError(self._errors)

    def __validate(self, fieldname, data, schema, path):

        if schema is not None:
            if not isinstance(schema, dict):
                raise SchemaError("Type for field '%s' must be 'dict', got: '%s'" %
                                  (fieldname, type(schema).__name__))

            add_required_rule = self.required_by_default and 'required' not in schema
            add_not_blank_rule = not self.blank_by_default and 'blank' not in schema

            if add_required_rule or add_not_blank_rule:
                newschema = copy.copy(schema)

                if add_required_rule:
                    newschema['required'] = self.required_by_default
                if add_not_blank_rule:
                    newschema['blank'] = self.blank_by_default
            else:
                newschema = schema

            # add default values first before checking for required fields
            if self.apply_default_to_data and 'default' in schema:
                try:
                    self.validate_type(x={'_ds': schema['default']}, fieldname='_ds',
                                       schema=schema,
                                       fieldtype=schema['type'] if 'type' in schema else None,
                                       path=path)
                except FieldValidationError as exc:
                    raise SchemaError(exc)

                if fieldname not in data:
                    data[fieldname] = schema['default']

            # iterate over schema and call all validators
            for schemaprop in newschema:
                validatorname = "validate_" + schemaprop
                validator = getattr(self, validatorname, None)
                if validator:
                    validator(data, fieldname, schema, path, newschema.get(schemaprop))

        return data
