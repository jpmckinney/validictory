#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from unittest import TestCase

import jsonschema

class TestMaximum(TestCase):
  
  props = {
    "prop01": { "type":"number",  "maximum":10 },
    "prop02": { "type":"integer", "maximum":20 }
  }
  schema = {"type": "object", "properties":props}
  
  
  def test_maximum_pass(self):
    
    #Test less than
    data1 = {
      "prop01": 5,
      "prop02": 10
    }
    
    #Test equal
    data2 = {
      "prop01": 10,
      "prop02": 20
    }
    
    try:
      jsonschema.validate(data1, self.schema)
      jsonschema.validate(data2, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_maximum_fail(self):
    
    #Test number
    data1 = {
      "prop01": 11,
      "prop02": 19
    }
    
    #Test integer
    data2 = {
      "prop01": 9,
      "prop02": 21
    }
    
    try:
      jsonschema.validate(data1, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))
    
    try:
      jsonschema.validate(data2, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))