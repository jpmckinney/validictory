from unittest import TestCase

import validictory


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

        validictory.validate(
            data, schema, required_by_default=False, apply_default_to_data=True)

        # Note: data was changed!
        self.assertEqual(data, {"foo": "bar", "baz": 2})

    # def test_item(self):
    #     schema = {
    #         'type': 'object',
    #         'type': 'array',
    #         'items': [
    #             {
    #                 'type': 'any'
    #             },
    #             {
    #                 'type': 'string'
    #             },
    #             {
    #                 'default': 'baz'
    #             },
    #         ]
    #     }

    #     data = ['foo', 'bar']

    #     validictory.validate(
    #         data, schema, required_by_default=False, apply_default_to_data=True)

    #     # Note: data was changed!
    #     self.assertEqual(data, ["foo", "bar", "baz"])

    def test_property_default_denied_does_not_change_original_data_on_error(self):
        schema = {
            "type": "object",
            "properties": {
                "foo": {
                    "type": "integer"
                },
                "bar": {
                    "type": "integer",
                    "default": 1
                }
            }
        }

        data = {"foo": "not_an_integer"}

        # the data does not match the schema and raises an error
        with self.assertRaises(validictory.FieldValidationError):
            validictory.validate(
                data, schema, required_by_default=False,
                apply_default_to_data=True)

        # the original data must not contain the default argument
        # because an error occurred
        self.assertEqual(data, {"foo": "not_an_integer"})

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

        # the original data MUST still be the same
        self.assertEqual(data, {})

        # TODO: DR I think a validictory.SchemaError should be raised instead
        # the default value provided does not match the type of the property
        # and raises an exception
        #with self.assertRaises(validictory.FieldValidationError):
        #    validictory.validate(
        #        data, schema, required_by_default=False,
        #        apply_default_to_data=True)
