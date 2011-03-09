Using validictory
=================

Normal use of validictory is as simple as calling :func:`validictory.validate`,
the only thing to learn is how to craft a schema.

For more example usage of all schema options check out the tests within 
``validictory/tests``.

Schema Options
--------------

``type``
    Validate that an item in the data is of a particular type.

    If a list of values is provided then any of the specified types
    will be accepted.

    Provided value can be any combination of the following:

    * ``string`` - str and unicode objects
    * ``integer`` - ints
    * ``number`` - ints and floats
    * ``boolean`` - bools
    * ``object`` - dicts
    * ``array`` - lists and tuples
    * ``null`` - None
    * ``any`` - any type is acceptable

``properties``
    List of validators for properties of the object.

    In essence each item in the provided dict for properties is a sub-schema
    applied against the property (if present) with the same name in the data.

``patternProperties``

    Define a set of patterns that validate against subschemas. 

    Similarly to how ``properties`` works, any properties in the data that have
    a name matching a particular pattern must validate against the provided
    sub-schema.

``additionalProperties``

    Schema for all additional properties not included in properties.

    Can be ``False`` to disallow any additional properties not in
    ``properties``, or can be a sub-schema that all properties
    not included in ``properties`` must match.

``items``
    Provide a schema or list of schemas to match against a list.

    If the provided value is a schema object then every item in the list
    will be validated against the given schema.

    If the provided value is a list of schemas then each item in the list
    must match the schema in the same position of the list.  (extra items
    will be validated according to ``additionalItems``)

``additionalItems``
    Used in conjunction with ``items``.  If False then no additional items
    are allowed, if a schema is provided then all additional items must
    match the provided schema.

``required``
    If True, the property must be present to validate.

    The default value of this parameter is set on the call to 
    :func:`~validictory.validate`.  By default it is ``True``.

.. note:: If you are following the JSON Schema spec, this diverges from the
          official spec as of v3.  If you want to validate against v3 more
          correctly, be sure to set ``required_by_default`` to False.

``dependencies``
    Can be a single string or list of strings representing properties
    that must exist if the given property exists.

For example::

    schema = {"prop01": {"required":False},
              "prop02": {"required":False, "dependencies":"prop01"}}

    # would validate
    {"prop01": 7}

    # would fail (missing prop01)
    {"prop02": 7}

``minimum`` and ``maximum``
    If the value is a number (int or float), these methods will validate
    that the values are less than or greater than the given minimum/maximum.

    Minimum and maximum values are inclusive by default.

``exclusiveMinimum`` and ``exclusiveMaximum``
    If these values are present and set to True, they will modify the
    ``minimum`` and ``maximum`` tests to be exclusive.

``minItems``, ``minLength``, ``maxItems``, and ``maxLength``
    If the value is a list or str, these will test the length of the list
    or string.

    There is no difference in implementation between the items/length variants.

``uniqueItems``
    Indicate that all attributes in a list must be unique.

``pattern``
    If the value is a string, this provides a regular expression that
    the string must match to be valid.

``enum``
    Provides an array that the value must match if present.

``format``
    Validate that the value matches a predefined format.

    By default several formats are recognized:

    * ``date-time``: 'yyyy-mm-ddhh:mm:ssZ'
    * ``date``: 'yyyy-mm-dd'
    * ``time``: 'hh:mm::ss'
    * ``utc-millisec``: number of seconds since UTC

    formats can be provided as the ``format_validators`` argument to
    ``validictory.validate``.

``divisibleBy``
    Ensures that the data value can be divided (without remainder) by a
    given divisor (**not 0**).

``title`` and ``description``
    These do no validation, but if provided must be strings or a
    ``~validictory.SchemaError`` will be raised.

