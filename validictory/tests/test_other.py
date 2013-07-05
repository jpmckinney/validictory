from unittest import TestCase

import validictory


class TestSchemaErrors(TestCase):

    def setUp(self):
        self.valid_desc = {"description": "My Description for My Schema"}
        self.invalid_desc = {"description": 1233}
        self.valid_title = {"title": "My Title for My Schema"}
        self.invalid_title = {"title": 1233}
        # doesn't matter what this is
        self.data = "whatever"

    def test_description_pass(self):
        self.assertEqual(list(validictory.validate(self.data, self.valid_desc)), [])

    def test_description_fail(self):
        self.assertRaises(validictory.SchemaError, validictory.validate, self.data, self.invalid_desc)

    def test_title_pass(self):
        self.assertEqual(list(validictory.validate(self.data, self.valid_title)), [])

    def test_title_fail(self):
        self.assertRaises(validictory.SchemaError, validictory.validate, self.data,
                          self.invalid_title)

    def test_invalid_type(self):
        data = {'bar': False}
        schema = {"type": "object", "required": True,
                  "properties": {"bar": "foo"}}
        try:
            list(validictory.validate(data, schema))
            assert False
        except Exception as e:
            self.assertEqual(type(e), validictory.SchemaError)
            self.assertEqual(str(e), "Type for field 'bar' must be 'dict', got: 'str'")


class TestFieldValidationErrors(TestCase):
    def setUp(self):
        self.schema = {"type": "object", "required": True,
                       "properties": {"bar": {"type": "integer"}}}

        self.data = {"bar": "faz"}

    def test(self):
        errors = list(validictory.validate(self.data, self.schema))
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].fieldname, "bar")
        self.assertEqual(errors[0].value, "faz")
