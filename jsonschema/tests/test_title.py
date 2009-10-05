import math
from unittest import TestCase

import jsonschema

class TestTitle(TestCase):
  
  schema = { "title":"My Title for My Schema" }
  schema2 = { "title": 1233 }
  
  def test_title_pass(self):
    
    #It shouldn't matter what this data is
    data = "whatever"
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_title_fail(self):
    
    #It shouldn't matter what this data is
    data = "whatever"
    
    try:
      jsonschema.validate(data, self.schema2)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))