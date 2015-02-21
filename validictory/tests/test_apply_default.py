from unittest import TestCase

import validictory


def validate_with_apply_default_to_data(data, schema):
    return validictory.validate(
        data,
        schema,
        required_by_default=True,
        apply_default_to_data=True
    )


class TestItemDefaults(TestCase):
    """ recognize a "default" keyword in a schema as a fallback for
    missing properties as described in
    http://json-schema.org/latest/json-schema-validation.html#anchor101
    """

    def test_property_default_is_applied(self):
        schema = {
            "type": "object",
            "properties": {
                "foo": {
                    "default": "bar"
                },
                "baz": {
                    "type": "integer"
                }
            }
        }

        data = {'baz': 2}

        validate_with_apply_default_to_data(data, schema)

        # Note: data was changed!
        self.assertEqual(data, {"foo": "bar", "baz": 2})

    def test_property_default_denied_if_wrong_type_for_default(self):
        schema = {
            "type": "object",
            "properties": {
                "foo": {
                    "type": "integer",
                    "default": "bar"
                }
            }
        }

        data = {}

        # from specification:
        # "There are no restrictions placed on the value of this keyword."
        # "It is RECOMMENDED that a default value be
        # valid against the associated schema."
        self.assertRaises(
            validictory.SchemaError,
            validate_with_apply_default_to_data,
            data,
            schema
        )

        # the original data is unchanged
        self.assertEqual(data, {})

    def test_property_default_with_wrong_default_raises_error_if_unused(self):
        schema = {
            "type": "object",
            "properties": {
                "foo": {
                    "type": "integer",
                    "default": "bar"
                }
            }
        }

        data = {'foo': 1}

        # The SchemaError is still raised because the schema is still wrong
        # even if the property is contained in the data
        self.assertRaises(
            validictory.SchemaError,
            validate_with_apply_default_to_data,
            data,
            schema
        )

        # the original data is unchanged
        self.assertEqual(data, {'foo': 1})
