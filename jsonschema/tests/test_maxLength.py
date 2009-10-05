import math
from unittest import TestCase

import jsonschema

class TestMaxLength(TestCase):
  
  schema = { "maxLength": 4 }
  
  def test_maxLength_pass(self):
    
    #test equal
    data1 = "test"
    
    #test less than
    data2 = "car"
    
    try:
      jsonschema.validate(data1, self.schema)
      jsonschema.validate(data2, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_maxLength_pass_nonstring(self):
    
    #test when data is not a string
    data1 = 12345
    data2 = [1, 2, "3", 4, 5]
    
    try:
      jsonschema.validate(data1, self.schema)
      jsonschema.validate(data2, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_maxLength_fail(self):
    
    #test equal
    data = "string"
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))