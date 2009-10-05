import math
from unittest import TestCase

import jsonschema

class TestMinLength(TestCase):
  
  schema = { "minLength": 4 }
  
  def test_minLength_pass(self):
    
    #test equal
    data1 = "test"
    
    #test greater than
    data2 = "string"
    
    try:
      jsonschema.validate(data1, self.schema)
      jsonschema.validate(data2, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_minLength_pass_nonstring(self):
    
    #test when data is not a string
    data1 = 123
    data2 = [1, 2, "3"]
    
    try:
      jsonschema.validate(data1, self.schema)
      jsonschema.validate(data2, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_minLength_fail(self):
    
    #test equal
    data = "car"
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))