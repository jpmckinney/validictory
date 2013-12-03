validictory changelog
=====================

0.9.4
-----
    * fix TypeError from format validators

0.9.3
-----
**2013-11-25**
    * fix bad 0.9.2 release that didn't have a fix for invalid code from a PR

0.9.2
-----
**2013-11-25**
    * fix from Marc Abramowitz for validating dict-like things as dicts
    * fix for patternProperties from Juan Menéndez & James Clemence
    * include implementation of "default" property from Daniel Rech
    * drop official support for Python 3.2
    * remove a test that relied on dict ordering
    * updated docs from  Mark Grandi
    * fix where format validators were cleared (also Mark Grandi)


0.9.1
-----
**2013-05-23**
    * fix for error message when data doesn't match one of multiple subtypes
    * fix for disallow_unknown_properties

0.9.0
-----
**2013-01-19**
    * remove optional and requires, deprecated in 0.6
    * improved additionalProperties error message
    * improved schema error message
    * add long to utc-millisec validation
    * accept Decimal where float is accepted
    * add FieldValidationError so that field names can be retrieved from error
    * a few Python 3 fixes

0.8.3
-----
**2012-03-13**
    * bugfix for Python 3: fix regression from 0.8.1 in use of long

0.8.2
-----
**2012-03-09**
    * doc improvements
    * PEP8 nearly everything
    * bugfix for patternProperties
    * ip-address should have been a format, not a type, breaks
      any code written depending on it in 0.8.1

0.8.1
-----
**2012-03-04**
    * add GeoJSON example to docs
    * allow longs in int/number validation
    * ignore additionalProperties for non-dicts
    * ip-address type validator

0.8.0
-----
**2012-01-26**
    * validate_enum accepts any container type
    * add support for Python 3
    * drop support for Python 2.5 and earlier

0.7.2
-----
**2011-09-27**
    * add blank_by_default argument
    * more descriptive error message for list items

0.7.1
-----
**2011-05-03**
    * PEP8 changes to code base
    * fix for combination of format & required=False
    * use ABCs to determine types in Python >= 2.6

0.7.0
-----
**2011-03-15**
    * fix dependencies not really supporting lists
    * add what might be the draft03 behavior for schema dependencies
    * add Sphinx documentation

0.6.1
-----
**2011-01-21**
    * bugfix for uniqueItems

0.6.0
-----
**2011-01-20**
    * more draft-03 stuff: patternProperties, additionalItems, exclusive{Minimum,Maximum}, divisibleBy
    * custom format validators
    * treat tuples as lists
    * replace requires with dependencies (deprecating requires)
    * replace optional with required (deprecating optional)
    * addition of required_by_default parameter

0.5.0
-----
**2011-01-13**
    * blank false by default
    * draft-03 stuff: uniqueItems, date formats

0.4.1
-----
**2010-08-27**
    * test custom types
    * optional defaults to False correctly
    * remove raise_errors
    * add value check in additionalProperties


0.4.0
-----
**2010-08-02**
    * renamed to validictory
    * removal of maxDecimal
    * ignore unknown attributes
    * differentiate between a schema error and a validation error
    * filter through _error
    * combine Items/Length checks
    * modular type checking
    * major test refactor

0.3.0
-----
**2010-07-29**
    * took over abandoned json_schema code
    * removal of interactive mode
    * PEP 8 cleanup of source
    * list/dict checks more flexible
    * remove identity/options/readonly junk
