#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from unittest import TestCase

import jsonschema

class TestType(TestCase):
    
    def test_schema(self):
      schema = { 
        "type": [
          { "type": "array",  "minItems": 10 },
          { "type": "string", "pattern": "^0+$" } 
        ]
      }
      
      data1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      data2 = "0";
      data3 = 1203;
      
      for x in [data1, data2]:
        try:
          jsonschema.validate(x, schema)
        except ValueError, e:
          self.fail("Unexpected failure: %s" % e)
      
      try:
        jsonschema.validate(data3, schema)
      except ValueError:
        pass
      else:
        self.fail("Expected failure for %s" % repr(x))
      
    def test_integer(self):
      for x in [1, 89, 48, 32, 49, 42]:
        try:
          jsonschema.validate(x, {"type":"integer"})
        except ValueError, e:
          self.fail("Unexpected failure: %s" % e)
      
      #failures
      for x in [1.2, "bad", {"test":"blah"}, [32, 49], None, True]:
        try:
          jsonschema.validate(x, {"type":"integer"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(x))
    
    def test_string(self):
      for x in ["surrender?", "nuts!", "ok", "@hsuha", "\'ok?\'", "blah"]:
        try:
          jsonschema.validate(x, {"type":"string"})
        except ValueError, e:
          self.fail("Unexpected failure: %s" % e)
      
      #failures
      for x in [1.2, 1, {"test":"blah"}, [32, 49], None, True]:
        try:
          jsonschema.validate(x, {"type":"string"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(x))
    
    def test_number(self):
      for x in [1.2, 89.42, 48.5224242, 32, 49, 42.24324]:
        try:
          jsonschema.validate(x, {"type":"number"})
        except ValueError, e:
          self.fail("Unexpected failure: %s" % e)
      
      #failures
      for x in ["bad", {"test":"blah"}, [32.42, 494242], None, True]:
        try:
          jsonschema.validate(x, {"type":"number"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(x))
    
    def test_boolean(self):
      for x in [True, False]:
        try:
          jsonschema.validate(x, {"type":"boolean"})
        except ValueError, e:
          self.fail("Unexpected failure: %s" % e)
      
      #failures
      for x in [1.2, "False", {"test":"blah"}, [32, 49], None, 1, 0]:
        try:
          jsonschema.validate(x, {"type":"boolean"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(x))
    
    def test_object(self):
      for x in [{"blah": "test"}, {"this":{"blah":"test"}}, {1:2, 10:20}]:
        try:
          jsonschema.validate(x, {"type":"object"})
        except ValueError, e:
          self.fail("Unexpected failure: %s" % e)
      
      #failures
      for x in [1.2, "bad", 123, [32, 49], None, True]:
        try:
          jsonschema.validate(x, {"type":"object"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(x))
    
    def test_array(self):
      for x in [[1, 89], [48, {"test":"blah"}, "49", 42]]:
        try:
          jsonschema.validate(x, {"type":"array"})
        except ValueError, e:
          self.fail("Unexpected failure: %s" % e)
      
      #failures
      for x in [1.2, "bad", {"test":"blah"}, 1234, None, True]:
        try:
          jsonschema.validate(x, {"type":"array"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(x))
    
    def test_null(self):
      
      try:
        jsonschema.validate(None, {"type":"null"})
      except ValueError, e:
        self.fail("Unexpected failure: %s" % e)
      
      #failures
      for x in [1.2, "bad", {"test":"blah"}, [32, 49], 1284, True]:
        try:
          jsonschema.validate(x, {"type":"null"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(x))
    
    def test_any(self):
      
      #test "any" and default value
      for y in [{"type": "any"}, {}]:
        for x in [1.2, "bad", {"test":"blah"}, [32, 49], None, 1284, True]:
          try:
            jsonschema.validate(x, y)
          except ValueError:
            self.fail("Unexpected failure: %s" % e)