import math
from unittest import TestCase

import jsonschema

class TestMaxLength(TestCase):

  schema = { "maxLength": 4 }

  def test_maxLength_pass(self):

    # str-equal, str-lt, list-equal, list-lt
    data = ["test", "car", [1,2,3,4], [0,0,0]]

    try:
        for item in data:
            jsonschema.validate(item, self.schema)
    except ValueError, e:
        self.fail("Unexpected failure: %s" % e)

  def test_maxLength_pass_nonstring(self):

    # test when data is not a string
    data1 = 12345

    try:
      jsonschema.validate(data1, self.schema)
    except ValueError, e:
      self.fail("Unexpected failure: %s" % e)

  def test_maxLength_fail(self):
    data = ["string", [1,2,3,4,5]]

    for item in data:
        self.assertRaises(ValueError, jsonschema.validate, item, self.schema)
