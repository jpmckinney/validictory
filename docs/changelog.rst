validictory changelog
=====================

0.7.1
-----
**unreleased**
    * PEP8 changes to code base
    * fix for combination of format & required=False


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
