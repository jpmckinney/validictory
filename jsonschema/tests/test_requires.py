#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from unittest import TestCase

import jsonschema

class TestRequires(TestCase):
  
  props = {
    "prop01": { "type":"string", "optional":True },
    "prop02": { "type":"number", "optional":True, "requires":"prop01" }
  }
  schema = {"type": "object", "properties":props}
  
  
  def test_requires_pass(self):
    
    data1 = {}
    data2 = {
      "prop01": "test",
      "prop02": 2
    }
    
    try:
      jsonschema.validate(data1, self.schema)
      jsonschema.validate(data2, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_requires_fail(self):
    
    data = {
      "prop02": 2
    }
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))