from unittest import TestCase

import validictory


class TestItems(TestCase):
    def test_property(self):
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

        result = validictory.validate(data, schema, required_by_default=False)
        self.assertEqual(result, {"foo": "bar", "baz": 2})

    def test_item(self):
        schema = {
            'type': 'object',
            'type': 'array',
            'items': [
                {
                    'type': 'any'
                },
                {
                    'type': 'string'
                },
                {
                    'default': 'baz'
                },
            ]
        }

        data = ['foo', 'bar']

        result = validictory.validate(data, schema, required_by_default=False)
        self.assertEqual(result, ["foo", "bar", "baz"])
