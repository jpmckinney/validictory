#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from unittest import TestCase

import jsonschema

class TestAdditionalProperties(TestCase):
    def test_no_properties(self):
      schema = {"additionalProperties":{"type":"integer"}}
      
      for x in [1, 89, 48, 32, 49, 42]:
        try:
          data = {"prop": x}
          jsonschema.validate(data, schema)
        except ValueError,e:
          self.fail("Unexpected failure: %s" % e)
          
      #failures
      for x in [1.2, "bad", {"test":"blah"}, [32, 49], None, True]:
        try:
          data = {"prop": x}
          jsonschema.validate(x, schema)
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %r" % None)
    
    def test_with_properties(self):
      schema = {
        "properties": {
          "prop1": {"type":"integer"},
          "prop2": {"type":"string"}
        },
        "additionalProperties":{"type":["string", "number"]}
      }
      
      for x in [1, "test", 48, "ok", 4.9, 42]:
        try:
          data = {
            "prop1":123,
            "prop2":"this is prop2",
            "prop3": x
          }
          jsonschema.validate(data, schema)
        except ValueError,e:
          self.fail("Unexpected failure: %s" % e)
          
      #failures
      for x in [{"test":"blah"}, [32, 49], None, True]:
        try:
          data = {
            "prop1":123,
            "prop2":"this is prop2",
            "prop3": x
          }
          jsonschema.validate(data, schema)
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %r" % None)
    
    def test_true(self):
      schema = {"additionalProperties":True}
      
      for x in [1.2, 1, {"test":"blah"}, [32, 49], None, True, "blah"]:
        try:
          data = {"prop": x}
          jsonschema.validate(data, schema)
        except ValueError, e:
          self.fail("Unexpected failure: %s" % e)
    
    def test_false(self):
      schema = {"additionalProperties":False}
      
      #failures
      for x in ["bad", {"test":"blah"}, [32.42, 494242], None, True, 1.34]:
        try:
          data = {"prop":x}
          jsonschema.validate(data, schema)
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(x))