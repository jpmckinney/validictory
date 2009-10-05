import math
from unittest import TestCase

import jsonschema

class TestPattern(TestCase):
  
  #Match a simplified regular expression for an e-mail address
  schema = { "pattern":"^[A-Za-z0-9][A-Za-z0-9\.]*@([A-Za-z0-9]+\.)+[A-Za-z0-9]+$" }
  
  def test_pattern_pass(self):
    
    data = "my.email01@gmail.com"
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_pattern_pass_nonstring(self):
    
    data = 123
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_pattern_fail(self):
    
    data = "whatever"
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))