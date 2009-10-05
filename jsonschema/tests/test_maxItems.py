import math
from unittest import TestCase

import jsonschema

class TestMaxItems(TestCase):
  
  schema = { "type": "array", "maxItems": 4 }
  schema2 = { "maxItems": 4 }
  
  def test_maxItems_pass(self):
    
    #test equal
    data1 = [1, 2, "3", 4.0]
    
    #test less than
    data2 = [1, 2, "3"]
    
    try:
      jsonschema.validate(data1, self.schema)
      jsonschema.validate(data2, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_maxItems_pass2(self):
    
    #test when data is not an array
    data1 = "test"
    
    #test arrays with no type attribute
    data2 = [1, 2, "3"]
    
    try:
      jsonschema.validate(data1, self.schema2)
      jsonschema.validate(data2, self.schema2)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_maxItems_fail(self):
    
    #test equal
    data1 = [1, 2, "3", 4.0, 5.00]
    
    try:
      jsonschema.validate(data1, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))
    
    try:
      jsonschema.validate(data1, self.schema2)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))