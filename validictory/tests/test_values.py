"""
    Tests that test the value of individual items
"""

from unittest import TestCase

import validictory


class TestEnum(TestCase):
    schema = {"enum":["test", True, 123, ["???"]]}

    def test_enum_pass(self):
        data = ["test", True, 123, ["???"]]
        try:
            for item in data:
                validictory.validate(item, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_enum_fail(self):
        data = "unknown"

        self.assertRaises(ValueError, validictory.validate, data, self.schema)


class TestPattern(TestCase):

    # match simplified regular expression for an e-mail address
    schema = {"pattern":
              "^[A-Za-z0-9][A-Za-z0-9\.]*@([A-Za-z0-9]+\.)+[A-Za-z0-9]+$"}

    def test_pattern_pass(self):
        data = "my.email01@gmail.com"

        try:
            validictory.validate(data, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_pattern_pass_nonstring(self):
        data = 123

        try:
            validictory.validate(data, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_pattern_fail(self):
        data = "whatever"

        self.assertRaises(ValueError, validictory.validate, data, self.schema)


class TestMaximum(TestCase):
    props = {
        "prop01": { "type":"number", "maximum":10 },
        "prop02": { "type":"integer", "maximum":20 }
    }
    schema = {"type": "object", "properties":props}

    def test_maximum_pass(self):
        #Test less than
        data1 = { "prop01": 5, "prop02": 10 }
        #Test equal
        data2 = { "prop01": 10, "prop02": 20 }

        try:
            validictory.validate(data1, self.schema)
            validictory.validate(data2, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_maximum_fail(self):
        #Test number
        data1 = { "prop01": 11, "prop02": 19 }
        #Test integer
        data2 = { "prop01": 9, "prop02": 21 }

        self.assertRaises(ValueError, validictory.validate, data1, self.schema)
        self.assertRaises(ValueError, validictory.validate, data2, self.schema)


class TestMinimum(TestCase):
    props = {
        "prop01": { "type":"number", "minimum":10 },
        "prop02": { "type":"integer", "minimum":20 }
    }
    schema = {"type": "object", "properties":props}

    def test_minimum_pass(self):
        #Test greater than
        data1 = { "prop01": 21, "prop02": 21 }
        #Test equal
        data2 = { "prop01": 10, "prop02": 20 }

        try:
            validictory.validate(data1, self.schema)
            validictory.validate(data2, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_minumum_fail(self):
        #Test number
        data1 = { "prop01": 9, "prop02": 21 }
        #Test integer
        data2 = { "prop01": 10, "prop02": 19 }

        self.assertRaises(ValueError, validictory.validate, data1, self.schema)
        self.assertRaises(ValueError, validictory.validate, data2, self.schema)


class TestMinLength(TestCase):
    schema = { "minLength": 4 }

    def test_minLength_pass(self):
        # str-equal, str-gt, list-equal, list-gt
        data = ['test', 'string', [1,2,3,4], [0,0,0,0,0]]

        try:
            for item in data:
                validictory.validate(item, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_minLength_pass_nonstring(self):
        #test when data is not a string
        data1 = 123

        try:
            validictory.validate(data1, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_minLength_fail(self):
        #test equal
        data = ["car", [1,2,3]]

        for item in data:
            self.assertRaises(ValueError, validictory.validate, data,
                              self.schema)


class TestMaxLength(TestCase):
    schema = { "maxLength": 4 }

    def test_maxLength_pass(self):
        # str-equal, str-lt, list-equal, list-lt
        data = ["test", "car", [1,2,3,4], [0,0,0]]
        try:
            for item in data:
                validictory.validate(item, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_maxLength_pass_nonstring(self):
        # test when data is not a string
        data1 = 12345

        try:
            validictory.validate(data1, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_maxLength_fail(self):
        data = ["string", [1,2,3,4,5]]
        for item in data:
            self.assertRaises(ValueError, validictory.validate, item,
                              self.schema)
