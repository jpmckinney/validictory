from unittest import TestCase

import validictory


class TestFailFast(TestCase):

    def test_multi_error(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
        }
        data = {"name": 2, "age": "fourty-two"}

        # ensure it raises an error
        self.assertRaises(validictory.ValidationError, validictory.validate,
                          data, schema, fail_fast=True)

        # ensure it raises a MultiError
        self.assertRaises(validictory.MultipleValidationError, validictory.validate,
                          data, schema, fail_fast=False)

        # ensure that the MultiError has 2 errors
        try:
            validictory.validate(data, schema, fail_fast=False)
        except validictory.MultipleValidationError as mve:
            assert len(mve.errors) == 2

    def test_multi_error_in_list(self):
        schema = {
            "type": "object",
            "properties": {
                "words": {"type": "array", "items": {"type": "string"}},
            },
        }
        data = {"words": ["word", 32, 2.1, True]}

        # ensure it raises an error
        self.assertRaises(validictory.ValidationError, validictory.validate,
                          data, schema, fail_fast=True)

        # ensure it raises a MultiError
        self.assertRaises(validictory.MultipleValidationError, validictory.validate,
                          data, schema, fail_fast=False)

        # ensure that the MultiError has 3 errors since 3 of the items were bad
        try:
            validictory.validate(data, schema, fail_fast=False)
        except validictory.MultipleValidationError as mve:
            assert len(mve.errors) == 3

    def test_multi_error_with_format(self):
        schema = {
            "type": "object",
            "properties": {
                "date": {"type": "string", "format": "date"},
                "time": {"type": "string", "format": "time"}
            },
        }
        data = {"date": "2011-02-99", "time": "30:00:00"}

        # ensure it raises an error
        self.assertRaises(validictory.ValidationError, validictory.validate,
                          data, schema, fail_fast=True)

        # ensure it raises a MultiError
        self.assertRaises(validictory.MultipleValidationError, validictory.validate,
                          data, schema, fail_fast=False)

        # ensure that the MultiError has 2 errors
        try:
            validictory.validate(data, schema, fail_fast=False)
        except validictory.MultipleValidationError as mve:
            assert len(mve.errors) == 2

    def test_no_error_with_type_list(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "sibling": {"type": ["string", "null"]}
            },
        }
        data = {"name": "john doe", "age": 42, "sibling": None}

        # this should not raise an error
        validictory.validate(data, schema, fail_fast=True)

        # and neither should this...fixed by dc78c
        validictory.validate(data, schema, fail_fast=False)

    def test_multi_error_with_type_list(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "sibling": {"type": ["string", "null"]}
            },
        }
        data = {"name": 2, "age": "fourty-two", "sibling": 0}

        # ensure it raises an error
        self.assertRaises(validictory.ValidationError, validictory.validate,
                          data, schema, fail_fast=True)

        # ensure it raises a MultiError
        self.assertRaises(validictory.MultipleValidationError, validictory.validate,
                          data, schema, fail_fast=False)

        # ensure that the MultiError has 3 errors
        try:
            validictory.validate(data, schema, fail_fast=False)
        except validictory.MultipleValidationError as mve:
            assert len(mve.errors) == 3
