#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from unittest import TestCase

import jsonschema

class TestMaxDecimal(TestCase):
  
  schema = { "type":"number",  "maxDecimal":3 }
  
  def test_maxDecimal_pass(self):
    
    #Test less than
    data1 = 10.20
    
    #Test equal
    data2 = 10.204
    
    try:
      jsonschema.validate(data1, self.schema)
      jsonschema.validate(data2, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_maxDecimal_fail(self):
    
    data1 = 10.04092
    
    try:
      jsonschema.validate(data1, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))