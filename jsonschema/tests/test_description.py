import math
from unittest import TestCase

import jsonschema

class TestDescription(TestCase):
  
  schema = { "description":"My Description for My Schema" }
  schema2 = { "description": 1233 }
  
  def test_description_pass(self):
    
    #It shouldn't matter what this data is
    data = "whatever"
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_description_fail(self):
    
    #It shouldn't matter what this data is
    data = "whatever"
    
    try:
      jsonschema.validate(data, self.schema2)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))