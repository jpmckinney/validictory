import math
from unittest import TestCase

import jsonschema

class TestEnum(TestCase):
  
  schema = {"enum":["test", True, 123, ["???"]]}
  
  def test_enum_pass(self):
    
    data1 = "test"
    data2 = True
    data3 = 123
    data4 = ["???"]
    
    try:
      jsonschema.validate(data1, self.schema)
      jsonschema.validate(data2, self.schema)
      jsonschema.validate(data3, self.schema)
      jsonschema.validate(data4, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_enum_fail(self):
    
    data = "unknown"
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(x))