#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from unittest import TestCase

import jsonschema

class TestItems(TestCase):
  
  schema1 = {
    "type": "array", 
    "items":{"type":"string"}
  }
  
  schema2 = {
    "type": "array", 
    "items":[{"type":"integer"}, {"type":"string"}, {"type":"boolean"}]
  }
  
  def test_items_single_pass(self):
    
    data = ["string", "another string", "mystring"]
    data2 = ["JSON Schema is cool", "yet another string"]
    
    try:
      jsonschema.validate(data, self.schema1)
      jsonschema.validate(data2, self.schema1)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_items_single_fail(self):
    
    data = ["string", "another string", 1]
    
    try:
      jsonschema.validate(data, self.schema1)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(x))
  
  def test_items_multiple_pass(self):
    
    data = [1, "More strings?", True]
    data2 = [12482, "Yes, more strings", False]
    
    try:
      jsonschema.validate(data, self.schema2)
      jsonschema.validate(data2, self.schema2)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_items_multiple_fail(self):
    
    data = [1294, "Ok. I give up"]
    
    try:
      jsonschema.validate(data, self.schema2)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(x))
    
    data = [1294, "Ok. I give up", "Not a boolean"]
    
    try:
      jsonschema.validate(data, self.schema2)
    except ValueError:
      pass
    else:
      self.fail("Expected failure for %s" % repr(x))