INTRO

jsonschema is a full featured validator for the JSON Schema specification.
It conforms to the JSON Schema Proposal Second Draft which can be found at the
following url:

http://groups.google.com/group/json-schema/web/json-schema-proposal---second-draft

INSTALL

jsonschema uses setup tools so it can be installed normally using:

python setup.py install

Furthermore, the test suite can be run by using the following command:

python setup.py test

USAGE

JSON documents and schema must first be loaded into a python dictionary type
before it can be validated. This can be done with the JSON parser of your choice
but I will use simplejson (just because).

Parsing a simple JSON document

>>> import jsonschema
>>> jsonschema.validate("simplejson", {"type":"string"})

Parsing a more complex JSON document.

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
ValueErrors are thrown when validation errors occur.

>>> import jsonschema
>>> try:
...     jsonschema.validate("simplejson", {"type":"string","minLength":15})
... except ValueError, e:
...     print e.message
... 
Length of 'simplejson' must be more than 15.000000

EXTENDING JSONSCHEMA

jsonschema provides an API similar to simplejson in that validators can be
overridden to support special property support or extended functionality. 
Samples of how jsonschema can be extended can be found in the examples
directory.

LIMITATIONS

References are currently not supported.
The unique property is currently not validated.
