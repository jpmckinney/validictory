import re

class SchemaError(ValueError):
    """errors relating to an invalid schema passed to validate"""

class ValidationError(ValueError):
    """validation errors encountered during validate"""

class JSONSchemaValidator(object):
    '''
    Implementation of the json-schema validator that adheres to the
    JSON Schema Proposal 2nd Draft.
    '''

    # Map of schema types to their equivalent in the python types module
    _typesmap = {
        "string": lambda x: isinstance(x, basestring),
        "integer": lambda x: type(x) == int,
        "number": lambda x: type(x) in (int, float),
        "boolean": lambda x: type(x) == bool,
        "object": lambda x: isinstance(x, dict),
        "array": lambda x: isinstance(x, list),
        "null": lambda x: x is None,
        "any": lambda x: True,
    }

    def _error(self, desc, value, fieldname, **params):
        params['value'] = value
        params['fieldname'] = fieldname
        raise ValidationError(desc % params)

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
        finally:
            value = x.get(fieldname)

        if fieldtype and fieldexists:
            if isinstance(fieldtype, list):
                # Match if type matches any one of the types in the list
                datavalid = False
                for eachtype in fieldtype:
                    try:
                        self.validate_type(x, fieldname, eachtype, eachtype)
                        datavalid = True
                        break
                    except ValidationError:
                        pass
                if not datavalid:
                    self._error("Value %(value)r for field '%(fieldname)s' is not of type %(fieldtype)s",
                                value, fieldname, fieldtype=fieldtype)
            elif isinstance(fieldtype, dict):
                try:
                    self.__validate(fieldname, x, fieldtype)
                except ValueError, e:
                    raise e
            else:
                fieldtype = str(fieldtype)
                if fieldtype in self._typesmap.keys():
                    type_checker = self._typesmap[fieldtype]
                else:
                    raise SchemaError("Field type '%s' is not supported." %
                                     fieldtype)

                if not type_checker(value):
                    self._error("Value %(value)r for field '%(fieldname)s' is not of type %(fieldtype)s",
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
                    for eachProp in properties.keys():
                        self.__validate(eachProp, value,
                                        properties.get(eachProp))
                else:
                    raise SchemaError("Properties definition of field '%s' is not an object" % fieldname)

    def validate_items(self, x, fieldname, schema, items=None):
        '''
        Validates that all items in the list for the given field match the
        given schema
        '''
        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if isinstance(value, list):
                if isinstance(items, list):
                    if len(items) == len(value):
                        for itemIndex in range(len(items)):
                            try:
                                self.validate(value[itemIndex], items[itemIndex])
                            except ValueError, e:
                                raise type(e)("Failed to validate field '%s' list schema: %s" % (fieldname, e))
                    else:
                        self._error("Length of list %(value)r for field '%(fieldname)s' is not equal to length of schema list",
                                    value, fieldname)
                elif isinstance(items, dict):
                    for eachItem in value:
                            try:
                                self._validate(eachItem, items)
                            except ValueError, e:
                                raise type(e)("Failed to validate field '%s' list schema: %s" % (fieldname, e))
                else:
                    raise SchemaError("Properties definition of field '%s' is not a list or an object" % fieldname)

    def validate_optional(self, x, fieldname, schema, optional=False):
        '''
        Validates that the given field is present if optional is false
        '''
        # Make sure the field is present
        if fieldname not in x.keys() and not optional:
            self._error("Required field '%(fieldname)s' is missing",
                        None, fieldname)

    def validate_additionalProperties(self, x, fieldname, schema,
                                      additionalProperties=None):
        '''
        Validates additional properties of a JSON object that were not
        specifically defined by the properties property
        '''
        # If additionalProperties is the boolean value True then we accept
        # any additional properties.
        if isinstance(additionalProperties, bool) and additionalProperties:
            return

        value = x.get(fieldname)
        if isinstance(additionalProperties, (dict, bool)):
            properties = schema.get("properties")
            if properties is None:
                properties = {}
            for eachProperty in value.keys():
                if eachProperty not in properties:
                    # If additionalProperties is the boolean value False
                    # then we don't accept any additional properties.
                    if (isinstance(additionalProperties, bool) and
                        not additionalProperties):
                        self._error("additional properties not defined by 'properties' are not allowed in field '%(fieldname)s'",
                                    None, fieldname)
                    self.__validate(eachProperty, value,
                                    additionalProperties)
        else:
            raise SchemaError("additionalProperties schema definition for field '%s' is not an object" % fieldname)

    def validate_requires(self, x, fieldname, schema, requires=None):
        if x.get(fieldname) is not None:
            if x.get(requires) is None:
                self._error("Field '%(requires)s' is required by field '%(fieldname)s'",
                            None, fieldname, requires=requires)

    def validate_minimum(self, x, fieldname, schema, minimum=None):
        '''
        Validates that the field is longer than or equal to the minimum
        length if specified
        '''
        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if value is not None:
                if type(value) in (int, float) and value < minimum:
                    self._error("Value %(value)r for field '%(fieldname)s' is less than minimum value: %(minimum)f",
                                value, fieldname, minimum=minimum)
                elif isinstance(value, list) and len(value) < minimum:
                    self._error("Value %(value)r for field '%(fieldname)s' has fewer values than the minimum: %(minimum)f",
                                value, fieldname, minimum=minimum)

    def validate_maximum(self, x, fieldname, schema, maximum=None):
        '''
        Validates that the field is shorter than or equal to the maximum
        length if specified.
        '''
        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if value is not None:
                if type(value) in (int, float) and value > maximum:
                    self._error("Value %(value)r for field '%(fieldname)s' is greater than maximum value: %(maximum)f",
                                value, fieldname, maximum=maximum)
                elif isinstance(value, list) and len(value) > maximum:
                    self._error("Value %(value)r for field '%(fieldname)s' has more values than the maximum: %(maximum)f",
                                value, fieldname, maximum=maximum)

    def validate_minItems(self, x, fieldname, schema, minitems=None):
        '''
        Validates that the number of items in the given field is equal to or
        more than the minimum amount.
        '''
        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if value is not None:
                if isinstance(value, list) and len(value) < minitems:
                    raise ValidationError("Value %r for field '%s' must have a minimum of %d items" % (fieldname, fieldname, minitems))

    def validate_maxItems(self, x, fieldname, schema, maxitems=None):
        '''
        Validates that the number of items in the given field is equal to or
        less than the maximum amount.
        '''
        if x.get(fieldname) is not None:
            value = x.get(fieldname)
            if value is not None:
                if isinstance(value, list) and len(value) > maxitems:
                    raise ValidationError("Value %r for field '%s' must have a maximum of %d items" % (value, fieldname, maxitems))

    def validate_maxLength(self, x, fieldname, schema, length=None):
        '''
        Validates that the value of the given field is shorter than or equal
        to the specified length if a string
        '''
        value = x.get(fieldname)
        if isinstance(value, basestring) and len(value) > length:
            raise ValidationError("Length of value %r for field '%s' must be less than or equal to %f" % (value, fieldname, length))

    def validate_minLength(self, x, fieldname, schema, length=None):
        '''
        Validates that the value of the given field is longer than or equal
        to the specified length if a string
        '''
        value = x.get(fieldname)
        if isinstance(value, basestring) and len(value) < length:
            raise ValidationError("Length of value %r for field '%s' must be more than or equal to %f" % (value, fieldname, length))

    def validate_pattern(self, x, fieldname, schema, pattern=None):
        '''
        Validates that the given field, if a string, matches the given
        regular expression.
        '''
        value = x.get(fieldname)
        if isinstance(value, basestring):
            p = re.compile(pattern)
            if not p.match(value):
                self._error("Value %(value)r for field '%(fieldname)s' does not match regular expression '%(pattern)s'",
                            value, fieldname, pattern=pattern)

    def validate_enum(self, x, fieldname, schema, options=None):
        '''
        Validates that the value of the field is equal to one of the
        specified option values
        '''
        value = x.get(fieldname)
        if value is not None:
            if not isinstance(options, list):
                raise SchemaError("Enumeration %r for field '%s' is not a list type", (options, fieldname))
            if value not in options:
                self._error("Value %(value)r for field '%(fieldname)s' is not in the enumeration: %(options)r",
                            value, fieldname, options=options)

    def validate_title(self, x, fieldname, schema, title=None):
        if not isinstance(title, (basestring, type(None))):
            raise SchemaError("The title for field '%s' must be a string" %
                             fieldname)

    def validate_description(self, x, fieldname, schema, description=None):
        if not isinstance(description, (basestring, type(None))):
            raise SchemaError("The description for field '%s' must be a string."
                             % fieldname)

    def validate_disallow(self, x, fieldname, schema, disallow=None):
        '''
        Validates that the value of the given field does not match the
        disallowed type.
        '''
        try:
            self.validate_type(x, fieldname, schema, disallow)
        except ValidationError:
            return
        self._error("Value %(value)r of type %(disallow)s is disallowed for field '%(fieldname)s'",
                    x.get(fieldname), fieldname, disallow=disallow)

    def validate(self, data, schema):
        '''
        Validates a piece of json data against the provided json-schema.
        '''
        self._validate(data, schema)

    def _validate(self, data, schema):
        self.__validate("_data", {"_data": data}, schema)

    def __validate(self, fieldname, data, schema):

        if schema is not None:
            if not isinstance(schema, dict):
                raise SchemaError("Schema structure is invalid.")

            for schemaprop in schema:

                validatorname = "validate_" + schemaprop

                validator = getattr(self, validatorname, None)
                if validator:
                    validator(data, fieldname, schema, schema.get(schemaprop))

        return data

__all__ = ['JSONSchemaValidator']
