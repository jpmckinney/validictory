from unittest import TestCase

import validictory


class TestProperties(TestCase):
    props = {
        "prop01": {"type": "string"},
        "prop02": {"type": "number", "required": False},
        "prop03": {"type": "integer"},
        "prop04": {"type": "boolean"},
        "prop05": {
            "type": "object",
            "required": False,
            "properties": {
                "subprop01": {"type": "string"},
                "subprop02": {"type": "string", "required": True}
            }
        }
    }
    schema = {"type": "object", "properties": props}

    def test_properties1(self):

        data = {
            "prop01": "test",
            "prop02": 1.20,
            "prop03": 1,
            "prop04": True,
            "prop05": {
                "subprop01": "test",
                "subprop02": "test2",
            }
        }

        self.assertEqual(list(validictory.validate(data, self.schema)), [])

    def test_properties2(self):

        data = {
            "prop01": "test",
            "prop02": 1.20,
            "prop03": 1,
            "prop04": True
        }

        self.assertEqual(list(validictory.validate(data, self.schema)), [])

    def test_properties3(self):
        data = {
            "prop02": 1.60,
            "prop05": {
                "subprop01": "test"
            }
        }

        self.assertEqual(len(list(validictory.validate(data, self.schema))), 4)


class TestPatternProperties(TestCase):
    schema = {'patternProperties': {'[abc]': {'type': 'boolean'}}}

    def test_patternproperties_pass(self):
        data = {'a': True}

        self.assertEqual(list(validictory.validate(data, self.schema)), [])

    def test_patternproperties_nonmatch(self):
        data = {'a': True, 'd': 'foo'}

        self.assertEqual(list(validictory.validate(data, self.schema)), [])

    def test_patternproperties_nested(self):
        schema = {'patternProperties': {'[abc]': {
            'patternProperties': {'[abc]': {'type': 'boolean'}}
        }}}

        data = {'a': {'b': False}}

        self.assertEqual(list(validictory.validate(data, schema)), [])

    def test_patternproperties_fail_multiple(self):
        data = {'a': True, 'b': False, 'c': 'foo'}
        self.assertEqual(len(list(validictory.validate(data, self.schema))), 1)

    def test_patternproperties_fail(self):
        data = {'a': 12}
        self.assertEqual(len(list(validictory.validate(data, self.schema))), 1)

    def test_patternproperties_missing(self):
        schema = {'properties': {'patprops': {
            'required': False, 'type': 'object',
            'patternProperties': {'[abc]': {'required': True,
                                            'type': 'array'}}
        }}}
        data = {'id': 1}
        self.assertEqual(list(validictory.validate(data, schema)), [])


class TestAdditionalProperties(TestCase):
    def test_no_properties(self):
        schema = {"additionalProperties": {"type": "integer"}}

        for x in [1, 89, 48, 32, 49, 42]:
            self.assertEqual(list(validictory.validate({"prop": x}, schema)), [])

        #failures
        for x in [1.2, "bad", {"test": "blah"}, [32, 49], None, True]:
            self.assertEqual(len(list(validictory.validate({"prop": x}, schema))), 1)

    def test_with_properties(self):
        schema = {
            "properties": {
                "prop1": {"type": "integer"},
                "prop2": {"type": "string"}
            },
            "additionalProperties": {"type": ["string", "number"]}
        }

        for x in [1, "test", 48, "ok", 4.9, 42]:
            data = {
                "prop1": 123,
                "prop2": "this is prop2",
                "prop3": x
            }
            self.assertEqual(list(validictory.validate(data, schema)), [])

        #failures
        for x in [{"test": "blah"}, [32, 49], None, True]:
            data = {
                "prop1": 123,
                "prop2": "this is prop2",
                "prop3": x
            }
            self.assertEqual(len(list(validictory.validate(data, schema))), 1)

    def test_true(self):
        schema = {"additionalProperties": True}

        for x in [1.2, 1, {"test": "blah"}, [32, 49], None, True, "blah"]:
            self.assertEqual(list(validictory.validate({"prop": x}, schema)), [])

    def test_false(self):
        schema = {"additionalProperties": False}

        for x in ["bad", {"test": "blah"}, [32.42, 494242], None, True, 1.34]:
            self.assertEqual(len(list(validictory.validate({"prop": x}, schema))), 1)

    def test_false_with_type_string(self):
        schema = {
            "type": ["object", "string"],
            "properties": {
                "key": {"type": "string"}
            },
            "additionalProperties": False
        }

        for data in ["foobar", {'key': 'value'}]:
            self.assertEqual(list(validictory.validate(data, schema)), [])

        #failures
        for data in [['foo', 'bar'], None, True]:
            self.assertEqual(len(list(validictory.validate(data, schema))), 1)
        self.assertEqual(len(list(validictory.validate({'roses': 'red'}, schema))), 2)


class TestDependencies(TestCase):
    props = {
        "prop01": {"type": "string", "required": False},
        "prop02": {"type": "number", "required": False,
                   "dependencies": "prop01"}
    }
    schema = {"type": "object", "properties": props}

    props_array = {
        "prop01": {"type": "string", "required": False},
        "prop02": {"type": "string", "required": False},
        "prop03": {"type": "number", "required": False,
                   "dependencies": ["prop01", "prop02"]}
    }
    schema_array = {"type": "object", "properties": props_array}

    def test_dependencies_pass(self):
        data1 = {}
        data2 = {"prop01": "test"}
        data3 = {"prop01": "test", "prop02": 2}
        data4 = {"prop01": "a", "prop02": "b", "prop03": 7}

        self.assertEqual(list(validictory.validate(data1, self.schema)), [])
        self.assertEqual(list(validictory.validate(data2, self.schema)), [])
        self.assertEqual(list(validictory.validate(data3, self.schema)), [])
        self.assertEqual(list(validictory.validate(data4, self.schema_array)), [])

    def test_dependencies_fail(self):
        data1 = {"prop02": 2}
        data2 = {"prop01": "x", "prop03": 7}

        self.assertEqual(len(list(validictory.validate(data1, self.schema))), 1)
        self.assertEqual(len(list(validictory.validate(data2, self.schema_array))), 1)


class TestRequired(TestCase):
    props = {
        "prop_def": {"type": "string"},
        "prop_opt": {"type": "number", "required": False},
        "prop_req": {"type": "boolean", "required": True}
    }
    schema = {"type": "object", "properties": props}

    def_and_req = {"prop_def": "test", "prop_req": False}
    req_only = {"prop_req": True}
    opt_only = {"prop_opt": 7}

    def test_required_pass(self):
        # should pass if def and req are there
        self.assertEqual(list(validictory.validate(self.def_and_req, self.schema)), [])
        # should pass if default is missing but req_by_default=False
        self.assertEqual(list(validictory.validate(self.req_only, self.schema,
                                 required_by_default=False)), [])

    def test_required_fail(self):
        # missing required should always fail
        self.assertEqual(len(list(validictory.validate(self.opt_only,
                          self.schema))), 2)
        self.assertEqual(len(list(validictory.validate(self.opt_only,
                          self.schema, required_by_default=False))), 1)
        # missing the default, fail if required_by_default=True
        self.assertEqual(len(list(validictory.validate(self.req_only,
                          self.schema))), 1)
