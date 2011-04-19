from unittest import TestCase

import validictory

class TestProperties(TestCase):
    props = {
        "prop01": {"type":"string"},
        "prop02": {"type":"number", "optional":True},
        "prop03": {"type":"integer"},
        "prop04": {"type":"boolean"},
        "prop05": {
            "type":"object",
            "optional":True,
            "properties": {
                "subprop01":{"type":"string"},
                "subprop02":{"type":"string", "optional":False}
            }
        }
    }
    schema = {"type": "object", "properties":props}

    def test_properties1(self):

        data = {
            "prop01": "test",
            "prop02": 1.20,
            "prop03": 1,
            "prop04": True,
            "prop05": {
                "subprop01":"test",
                "subprop02":"test2",
            }
        }

        try:
            validictory.validate(data, self.schema)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_properties2(self):

        data = {
            "prop01": "test",
            "prop02": 1.20,
            "prop03": 1,
            "prop04": True
        }

        try:
            validictory.validate(data, self.schema)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_properties3(self):
        data = {
            "prop02":1.60,
            "prop05": {
                "subprop01":"test"
            }
        }

        self.assertRaises(ValueError, validictory.validate, data, self.schema)

class TestPatternProperties(TestCase):
    schema = { 'patternProperties': { '[abc]': { 'type': 'boolean' } } }

    def test_patternproperties_pass(self):
        data = { 'a': True }

        try:
            validictory.validate(data, self.schema)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_patternproperties_nonmatch(self):
        data = { 'a': True, 'd': 'foo' }

        try:
            validictory.validate(data, self.schema)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_patternproperties_nested(self):
        schema = { 'patternProperties': { '[abc]': {
                     'patternProperties': { '[abc]': { 'type': 'boolean' } }
                  } } }

        data = { 'a': {'b': False }}

        try:
            validictory.validate(data, schema)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_patternproperties_fail_multiple(self):
        data = { 'a': True, 'b': False, 'c': 'foo' }
        self.assertRaises(ValueError, validictory.validate, data, self.schema)

    def test_patternproperties_fail(self):
        data = { 'a': 12 }
        self.assertRaises(ValueError, validictory.validate, data, self.schema)


class TestAdditionalProperties(TestCase):
    def test_no_properties(self):
        schema = {"additionalProperties":{"type":"integer"}}

        for x in [1, 89, 48, 32, 49, 42]:
            try:
                data = {"prop": x}
                validictory.validate(data, schema)
            except ValueError as e:
                self.fail("Unexpected failure: %s" % e)

        #failures
        for x in [1.2, "bad", {"test":"blah"}, [32, 49], None, True]:
            self.assertRaises(ValueError, validictory.validate, {"prop": x},
                              schema)

    def test_with_properties(self):
        schema = {
            "properties": {
                "prop1": {"type":"integer"},
                "prop2": {"type":"string"}
            },
            "additionalProperties":{"type":["string", "number"]}
        }

        for x in [1, "test", 48, "ok", 4.9, 42]:
            try:
                data = {
                    "prop1":123,
                    "prop2":"this is prop2",
                    "prop3": x
                }
                validictory.validate(data, schema)
            except ValueError as e:
                self.fail("Unexpected failure: %s" % e)

        #failures
        for x in [{"test":"blah"}, [32, 49], None, True]:
            data = {
                "prop1":123,
                "prop2":"this is prop2",
                "prop3": x
            }
            self.assertRaises(ValueError, validictory.validate, data, schema)

    def test_true(self):
        schema = {"additionalProperties":True}

        for x in [1.2, 1, {"test":"blah"}, [32, 49], None, True, "blah"]:
            try:
                validictory.validate({"prop": x}, schema)
            except ValueError as e:
                self.fail("Unexpected failure: %s" % e)

    def test_false(self):
        schema = {"additionalProperties":False}

        for x in ["bad", {"test":"blah"}, [32.42, 494242], None, True, 1.34]:
            self.assertRaises(ValueError, validictory.validate, {"prop":x},
                              schema)


class TestRequires(TestCase):
    '''
    "requires" is deprecated in draft-03 and replaced by "dependencies"
    '''

    props = {
        "prop01": { "type":"string", "optional":True },
        "prop02": { "type":"number", "optional":True, "requires":"prop01" }
    }
    schema = {"type": "object", "properties":props}

    def test_requires_pass(self):
        data1 = {}
        data2 = { "prop01": "test" }
        data3 = { "prop01": "test", "prop02": 2 }

        try:
            validictory.validate(data1, self.schema)
            validictory.validate(data2, self.schema)
            validictory.validate(data3, self.schema)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_requires_fail(self):
        data = { "prop02": 2 }

        self.assertRaises(ValueError, validictory.validate, data, self.schema)

class TestDependencies(TestCase):
    props = {
        "prop01": { "type":"string", "optional":True },
        "prop02": { "type":"number", "optional":True, "dependencies":"prop01" }
    }
    schema = {"type": "object", "properties":props}

    props_array = {
        "prop01": { "type":"string", "optional":True },
        "prop02": { "type":"string", "optional":True },
        "prop03": { "type":"number", "optional":True, "dependencies": ["prop01", "prop02"] }
    }
    schema_array = {"type": "object", "properties":props_array}

    def test_dependencies_pass(self):
        data1 = {}
        data2 = { "prop01": "test" }
        data3 = { "prop01": "test", "prop02": 2 }
        data4 = { "prop01": "a", "prop02": "b", "prop03": 7 }

        try:
            validictory.validate(data1, self.schema)
            validictory.validate(data2, self.schema)
            validictory.validate(data3, self.schema)
            validictory.validate(data4, self.schema_array)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_dependencies_fail(self):
        data1 = { "prop02": 2 }
        data2 = { "prop01": "x", "prop03": 7}

        self.assertRaises(ValueError, validictory.validate, data1, self.schema)
        self.assertRaises(ValueError, validictory.validate, data2,
                          self.schema_array)

class TestOptional(TestCase):
    props = {
        "prop01": {"type":"string"},
        "prop02": {"type":"number", "optional":True},
        "prop03": {"type":"integer"},
        "prop04": {"type":"boolean", "optional":False}
    }
    schema = {"type": "object", "properties":props}

    def test_optional_pass(self):
        x = {
            "prop01":"test",
            "prop03": 1,
            "prop04": False
        }

        try:
            validictory.validate(x, self.schema)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_optional_fail(self):
        x = { "prop02":"blah" }
        self.assertRaises(ValueError, validictory.validate, x, self.schema)
        x = { "prop04":True }  # should still fail
        self.assertRaises(ValueError, validictory.validate, x, self.schema)


class TestRequired(TestCase):
    props = {
        "prop_def": {"type":"string"},
        "prop_opt": {"type":"number", "required":False},
        "prop_req": {"type":"boolean", "required":True}
    }
    schema = {"type": "object", "properties":props}

    def_and_req = {"prop_def": "test", "prop_req": False}
    req_only = {"prop_req": True}
    opt_only = {"prop_opt": 7}

    def test_required_pass(self):
        try:
            # should pass if def and req are there
            validictory.validate(self.def_and_req, self.schema)
            # should pass if default is missing but req_by_default=False
            validictory.validate(self.req_only, self.schema,
                                 required_by_default=False)
        except ValueError as e:
            self.fail("Unexpected failure: %s" % e)

    def test_required_fail(self):
        # missing required should always fail
        self.assertRaises(ValueError, validictory.validate, self.opt_only,
                          self.schema)
        self.assertRaises(ValueError, validictory.validate, self.opt_only,
                          self.schema, required_by_default=False)
        # missing the default, fail if required_by_default=True
        self.assertRaises(ValueError, validictory.validate, self.req_only,
                          self.schema)
