import math
from unittest import TestCase

import jsonschema

class TestMinLength(TestCase):

  schema = { "minLength": 4 }

  def test_minLength_pass(self):

    # str-equal, str-gt, list-equal, list-gt
    data = ['test', 'string', [1,2,3,4], [0,0,0,0,0]]

    try:
      for item in data:
        jsonschema.validate(item, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)

  def test_minLength_pass_nonstring(self):

    #test when data is not a string
    data1 = 123

    try:
      jsonschema.validate(data1, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)

  def test_minLength_fail(self):

    #test equal
    data = ["car", [1,2,3]]

    for item in data:
        self.assertRaises(ValueError, jsonschema.validate, data, self.schema)
