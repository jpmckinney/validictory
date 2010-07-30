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
        except ValueError, e:
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
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_properties3(self):
        data = {
            "prop02":1.60,
            "prop05": {
                "subprop01":"test"
            }
        }

        self.assertRaises(ValueError, validictory.validate, data, self.schema)


class TestAdditionalProperties(TestCase):
    def test_no_properties(self):
        schema = {"additionalProperties":{"type":"integer"}}

        for x in [1, 89, 48, 32, 49, 42]:
            try:
                data = {"prop": x}
                validictory.validate(data, schema)
            except ValueError,e:
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
            except ValueError,e:
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
            except ValueError, e:
                self.fail("Unexpected failure: %s" % e)

    def test_false(self):
        schema = {"additionalProperties":False}

        for x in ["bad", {"test":"blah"}, [32.42, 494242], None, True, 1.34]:
            self.assertRaises(ValueError, validictory.validate, {"prop":x},
                              schema)


class TestRequires(TestCase):
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
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_requires_fail(self):
        data = { "prop02": 2 }

        self.assertRaises(ValueError, validictory.validate, data, self.schema)


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
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_optional_fail(self):
        x = {
            "prop02":"blah"
        }

        self.assertRaises(ValueError, validictory.validate, x, self.schema)
