#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from unittest import TestCase

import jsonschema

class TestOptional(TestCase):
  
  props = {
    "prop01": {"type":"string"},
    "prop02": {"type":"number", "optional":True},
    "prop03": {"type":"integer"},
    "prop04": {"type":"boolean", "optional":False}
  }
  schema = {"type": "object", "properties":props}
  
  
  def test_optional1(self):
    
    x = {
      "prop01":"test",
      "prop03": 1,
      "prop04": False
    }
    
    try:
      jsonschema.validate(x, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_optional2(self):
    
    x = {
      "prop02":"blah"
    }
    
    try:
      jsonschema.validate(x, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(None))