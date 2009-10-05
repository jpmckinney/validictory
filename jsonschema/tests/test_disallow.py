#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from unittest import TestCase

import jsonschema

class TestDisallow(TestCase):
    def test_integer(self):
      for x in [1, 89, 48, 32, 49, 42]:
        try:
          jsonschema.validate(x, {"disallow":"integer"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(None))
      
      #failures
      for x in [1.2, "bad", {"test":"blah"}, [32, 49], None, True]:
        try:
          jsonschema.validate(x, {"disallow":"integer"})
        except ValueError:
          self.fail("Unexpected failure: %s" % e)
    
    def test_string(self):
      for x in ["surrender?", "nuts!", "ok", "@hsuha", "\'ok?\'", "blah"]:
        try:
          jsonschema.validate(x, {"disallow":"string"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(None))
      
      #failures
      for x in [1.2, 1, {"test":"blah"}, [32, 49], None, True]:
        try:
          jsonschema.validate(x, {"disallow":"string"})
        except ValueError:
          self.fail("Unexpected failure: %s" % e)
    
    def test_number(self):
      for x in [1.2, 89.42, 48.5224242, 32, 49, 42.24324]:
        try:
          jsonschema.validate(x, {"disallow":"number"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(None))
      
      #failures
      for x in ["bad", {"test":"blah"}, [32.42, 494242], None, True]:
        try:
          jsonschema.validate(x, {"disallow":"number"})
        except ValueError:
          self.fail("Unexpected failure: %s" % e)
    
    def test_boolean(self):
      for x in [True, False]:
        try:
          jsonschema.validate(x, {"disallow":"boolean"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(None))
      
      #failures
      for x in [1.2, "False", {"test":"blah"}, [32, 49], None, 1, 0]:
        try:
          jsonschema.validate(x, {"disallow":"boolean"})
        except ValueError:
          self.fail("Unexpected failure: %s" % e)
    
    def test_object(self):
      for x in [{"blah": "test"}, {"this":{"blah":"test"}}, {1:2, 10:20}]:
        try:
          jsonschema.validate(x, {"disallow":"object"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(None))
      
      #failures
      for x in [1.2, "bad", 123, [32, 49], None, True]:
        try:
          jsonschema.validate(x, {"disallow":"object"})
        except ValueError:
          self.fail("Unexpected failure: %s" % e)
    
    def test_array(self):
      for x in [[1, 89], [48, {"test":"blah"}, "49", 42]]:
        try:
          jsonschema.validate(x, {"disallow":"array"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(None))
      
      #failures
      for x in [1.2, "bad", {"test":"blah"}, 1234, None, True]:
        try:
          jsonschema.validate(x, {"disallow":"array"})
        except ValueError:
          self.fail("Unexpected failure: %s" % e)
    
    def test_null(self):
      
      try:
        jsonschema.validate(None, {"disallow":"null"})
      except ValueError:
        pass
      else:
        self.fail("Expected failure for %s" % repr(None))
      
      #failures
      for x in [1.2, "bad", {"test":"blah"}, [32, 49], 1284, True]:
        try:
          jsonschema.validate(x, {"disallow":"null"})
        except ValueError:
          self.fail("Unexpected failure: %s" % e)
    
    def test_any(self):
      
      #test "any" and default value
      for x in [1.2, "bad", {"test":"blah"}, [32, 49], None, 1284, True]:
        try:
          jsonschema.validate(x, {"disallow":"any"})
        except ValueError:
          pass
        else:
          self.fail("Expected failure for %s" % repr(None))
            
    def test_multi(self):
      
      schema = {"disallow":["null", "integer", "string"]}
      try:
        jsonschema.validate(None, schema)
      except ValueError:
        pass
      else:
        self.fail("Expected failure for %s" % repr(None))
      
      try:
        jsonschema.validate(183, schema)
      except ValueError:
        pass
      else:
        self.fail("Expected failure for %s" % repr(None))
      
      try:
        jsonschema.validate("mystring", schema)
      except ValueError:
        pass
      else:
        self.fail("Expected failure for %s" % repr(None))
      
      #failures
      for x in [1.2, {"test":"blah"}, [32, 49], True]:
        try:
          jsonschema.validate(x, schema)
        except ValueError:
          self.fail("Unexpected failure: %s" % e)