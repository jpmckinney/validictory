#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from unittest import TestCase

import jsonschema

class TestProperties(TestCase):
  props = {
    "prop01": {"type":"string"},
    "prop02": {"type":"number", "optional":True},
    "prop03": {"type":"integer"},
    "prop04": {"type":"boolean"},
    "prop05": {
      "type":"object",
      "optional":True,
      "properties": {
        "subprop01":{"type":"string"},
        "subprop02":{"type":"string", "optional":False}
      }
    }
  }
  schema = {"type": "object", "properties":props}
  
  def test_properties1(self):
    
    data = {
      "prop01": "test",
      "prop02": 1.20,
      "prop03": 1,
      "prop04": True,
      "prop05": {
        "subprop01":"test",
        "subprop02":"test2",
      }
    }
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_properties2(self):
    
    data = {
      "prop01": "test",
      "prop02": 1.20,
      "prop03": 1,
      "prop04": True
    }
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
    
  def test_properties3(self):
    
    data = {
      "prop02":1.60,
      "prop05": {
        "subprop01":"test"
      }
    }
    
    try:
      jsonschema.validate(data, self.schema)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(x))