from unittest import TestCase

import validictory
from copy import deepcopy


class TestRemoveUnknownProperties(TestCase):

    def setUp(self):
        self.data_simple = {"name": "john doe", "age": 42}
        self.schema_simple = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
        }

        self.data_complex = {
            "inv_number": "123",
            "rows": [
                {
                    "sku": "ab-456",
                    "desc": "a description",
                    "price": 100.45
                },
                {
                    "sku": "xy-123",
                    "desc": "another description",
                    "price": 999.00
                }
            ]
        }
        self.schema_complex = {
            "type": "object",
            "properties": {
                "inv_number": {"type": "string"},
                "rows": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "sku": {"type": "string"},
                            "desc": {"type": "string"},
                            "price": {"type": "number"}
                        }
                    },
                }
            }
        }

    def test_remove_unknown_properties_pass(self):
        extra_data = deepcopy(self.data_simple)
        extra_data["sex"] = "male"
        validictory.validate(extra_data, self.schema_simple,
                             remove_unknown_properties=True)
        self.assertEqual(extra_data, self.data_simple)

    def test_remove_unknown_properties_patternproperties(self):
        schema = {
            "type": "object",
            "patternProperties": {
                "[abc]": {"type": "boolean"},
            },
            "properties": {
                "d": {"type": "boolean"},
            }
        }
        orig_data = {'a': True, 'b': False, 'd': True}
        data = deepcopy(orig_data)

        validictory.validate(data, schema, remove_unknown_properties=True)
        self.assertEqual(data, orig_data)

    def test_remove_unknown_properties_complex_pass(self):
        try:
            validictory.validate(self.data_complex, self.schema_complex,
                                 remove_unknown_properties=True)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_remove_unknown_properties_complex_fail(self):
        extra_data = deepcopy(self.data_complex)
        newrow_invalid = {"sku": "789", "desc": "catch me if you can", "price": 1,
                          "rice": 666}
        newrow_valid = {"sku": "789", "desc": "catch me if you can", "price": 1}

        extra_data["rows"].append(newrow_invalid)
        validictory.validate(extra_data, self.schema_complex,
                             remove_unknown_properties=True)
        self.data_complex["rows"].append(newrow_valid)
        self.assertEqual(extra_data, self.data_complex)
