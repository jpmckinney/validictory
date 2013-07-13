from unittest import TestCase

import validictory

schema = {
    "$schema": "http://json-schema.org/draft-03/schema#",
    "id": "http://json-schema.org/draft-03/schema#",
    "type": "object",

    "properties": {
        "type": {
            "type": ["string", "array"],
            "items": {
                "type": ["string", {"$ref": "#"}]
            },
            "uniqueItems": True,
            "default": "any"
        },

        "properties": {
            "type": "object",
            "additionalProperties": {"$ref": "#"},
            "default": {}
        },

        "patternProperties": {
            "type": "object",
            "additionalProperties": {"$ref": "#"},
            "default": {}
        },

        "additionalProperties": {
            "type": [{"$ref": "#"}, "boolean"],
            "default": {}
        },

        "items": {
            "type": [{"$ref": "#"}, "array"],
            "items": {"$ref": "#"},
            "default": {}
        },

        "additionalItems": {
            "type": [{"$ref": "#"}, "boolean"],
            "default": {}
        },

        "required": {
            "type": "boolean",
            "default": False
        },

        "dependencies": {
            "type": "object",
            "additionalProperties": {
                "type": ["string", "array", {"$ref": "#"}],
                "items": {
                    "type": "string"
                }
            },
            "default": {}
        },

        "minimum": {
            "type": "number"
        },

        "maximum": {
            "type": "number"
        },

        "exclusiveMinimum": {
            "type": "boolean",
            "default": False
        },

        "exclusiveMaximum": {
            "type": "boolean",
            "default": False
        },

        "minItems": {
            "type": "integer",
            "minimum": 0,
            "default": 0
        },

        "maxItems": {
            "type": "integer",
            "minimum": 0
        },

        "uniqueItems": {
            "type": "boolean",
            "default": False
        },

        "pattern": {
            "type": "string",
            "format": "regex"
        },

        "minLength": {
            "type": "integer",
            "minimum": 0,
            "default": 0
        },

        "maxLength": {
            "type": "integer"
        },

        "enum": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True
        },

        "default": {
            "type": "any"
        },

        "title": {
            "type": "string"
        },

        "description": {
            "type": "string"
        },

        "format": {
            "type": "string"
        },

        "divisibleBy": {
            "type": "number",
            "minimum": 0,
            "exclusiveMinimum": True,
            "default": 1
        },

        "disallow": {
            "type": ["string", "array"],
            "items": {
                "type": ["string", {"$ref": "#"}]
            },
            "uniqueItems": True
        },

        "extends": {
            "type": [{"$ref": "#"}, "array"],
            "items": {"$ref": "#"},
            "default": {}
        },

        "id": {
            "type": "string",
            "format": "uri"
        },

        "$ref": {
            "type": "string",
            "format": "uri"
        },

        "$schema": {
            "type": "string",
            "format": "uri"
        }
    },

    "dependencies": {
        "exclusiveMinimum": "minimum",
        "exclusiveMaximum": "maximum"
    },

    "default": {}
}


class TestSchemaSchema(TestCase):

    def test_schema(self):
        self.assertEqual(list(validictory.validate(schema, schema, required_by_default=False)), [])
