from unittest import TestCase

import validictory


class TestSchemaErrors(TestCase):

    valid_desc = {"description": "My Description for My Schema"}
    invalid_desc = {"description": 1233}
    valid_title = {"title": "My Title for My Schema"}
    invalid_title = {"title": 1233}
    # doesn't matter what this is
    data = "whatever"

    def test_description_pass(self):
        try:
            validictory.validate(self.data, self.valid_desc)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_description_fail(self):
        self.assertRaises(ValueError, validictory.validate, self.data,
                          self.invalid_desc)

    def test_title_pass(self):
        try:
            validictory.validate(self.data, self.valid_title)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_title_fail(self):
        self.assertRaises(ValueError, validictory.validate, self.data,
                          self.invalid_title)
