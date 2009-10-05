import math
from unittest import TestCase

import jsonschema

class TestDefault(TestCase):
  
  schema = { "properties":{"test":{"optional":True, "default":10}}}
  schema2 = { "properties":{"test":{"optional":True, "default":10, "readonly":True}}}
  
  def test_default_pass_set(self):
    
    data = {}
    
    try:
      jsonschema.validate(data, self.schema)
      if (data.get("test") != 10):
        self.fail("Default value was not set")
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_default_pass_noset(self):
    
    data = {}
    
    try:
      jsonschema.validate(data, self.schema2)
      if (data.get("test") == 10):
        self.fail("Default value was set when the schema indicates it should be readonly")
    except ValueError:
      self.fail("Unexpected failure: %s" % e)
  
  def test_default_interactive(self):
    
    data = {}
    
    try:
      # Explicitly set the interactive_mode
      jsonschema.validate(data, self.schema, interactive_mode=True)
      if (data.get("test") != 10):
        self.fail("Default value was not set")
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)
  
  def test_default_non_interactive(self):
    
    data = {}
    
    try:
      jsonschema.validate(data, self.schema, interactive_mode=False)
      if (data.get("test") == 10):
        self.fail("Default value was set when in non-interactive mode.")
    except ValueError:
      self.fail("Unexpected failure: %s" % e)