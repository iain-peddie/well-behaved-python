#!/usr/bin/env python3

# Copyright 2013 Iain Peddie inr314159@hotmail.com
# 
#    This file is part of WellBehavedPython
#
#    WellBehavedPython is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WellBehavedPython is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WellBehavedPython. If not, see <http://www.gnu.org/licenses/>.

from WellBehavedPython.TestCase import *
from WellBehavedPython.TestSuite import *
from WellBehavedPython.Expect import *

class ExpectTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_expects_fail_throws_AssertionError(self):
        # This would be easier if there was an expected exception,
        # but that comes later
        raised = True
        try:
            Expect(True).fail()
            raised = False
        except AssertionError:
            pass
        
        # Fail is so fundamental that we don't bootstrap
        # the asertion with Expect.toBeTrue() as that uses fail
        assert raised, "Expected an AssertionError to have been thrown"

    def test_failure_stores_message_if_provided(self):
        raised = True
        try:
            Expect(True).fail("ExpectedMessage")
            raised = False
        except AssertionError as ex:
            assert ex.args[0] == "ExpectedMessage"
        
        assert raised, "expected message not stored in exception"

    def test_equals_doesnt_raise_if_numeric_items_are_equal(self):
        Expect(1).toEqual(1)

    def test_equals_raises_with_right_message_if_numeric_items_not_equal(self):
        raised = True
        try:
            Expect(1).toEqual(2)
            raised = False
        except AssertionError as ex:
            # We use a manual assert here, otherwise we assume that toEqual works
            # in the test that's checking that it works
            assert ex.args[0] == "Expected 1 to equal 2", ex.args[0]
        
        
        Expect(raised).toBeTrue("Expected exception to be thrown")

    def test_equals_message_prepended_to_assert_message(self):
        raised = True
        try:
            Expect(1).toEqual(2, "first assert")
            raised = False
        except AssertionError as ex:
            # We use a manual assert here, otherwise we assume that toEqual works
            # in the test that's checking that it works
            assert ex.args[0] == "first assert: Expected 1 to equal 2", ex.args[0]
        
        Expect(raised).toBeTrue("Expected AssertionError to be raised")

    def test_equals_doesnt_raise_if_string_items_are_equal(self):
        Expect("hello").toEqual("hello")

    def test_equals_raises_with_right_message_if_string_items_not_equal(self):
        raised = True
        try:
            Expect("hello").toEqual("world")
            raised = False
        except AssertionError as ex:
            # We use a manual assert here. Otherwise we're assuming the code we're
            # testing here is already working. Which would be crazy.
            expected = "Expected 'hello' to equal 'world'"
            actual = ex.args[0]
            message = "'{}' != '{}'".format(expected, ex.args[0])
            assert actual == expected, message
        
        Expect(raised).toBeTrue("Expected exception to be thrown")

    def test_expects_not_toequal_behaves_correctly(self):
        Expect(1).Not.toEqual(2)

    def test_expecting_string1_to_equal_double1_fails(self):
        raised = False
        try:
            Expect("1").toEqual(1)
        except AssertionError as ex:
            raised = True
            Expect(ex.args[0]).toEqual("Cannot compare instance of <class 'str'> to "
                                       + "instance of <class 'int'> because their types differ")
        
        Expect(raised).toBeTrue("Expected AssertionError to be raised")

    def test_expect_truthy_values_to_be_true_succeeds(self):
        Expect(True).toBeTrue()
        Expect(1).toBeTrue()
        Expect((1)).toBeTrue()

    def test_expect_falsy_values_to_be_true_fails(self):
        values = (False, 0, ())
        actualMessages = []
        expectedMessages = ("Expected False to be True", 
                            "Expected 0 to be True",
                            "Expected () to be True")
        for value in values:
            try:
                Expect(value).toBeTrue()
            except AssertionError as ex:
                actualMessages.append(ex.args[0])
        
        Expect(len(actualMessages)).toEqual(3)
        for i in range(0,2):
            Expect(actualMessages[i]).toEqual(expectedMessages[i], "i = {}".format(i))

    def test_expect_truthy_values_to_be_false_fails(self):
        values = (True, 1, (1))
        actualMessages = []
        expectedMessages = ("Expected True to be False",
                            "Expected 1 to be False",
                            "Expected (1) to be False")

        for value in values:
            try:
                Expect(value).toBeFalse()
            except AssertionError as ex:
                actualMessages.append(ex.args[0])

        Expect(len(actualMessages)).toEqual(3)
        for i in range(0, 2):
            Expect(actualMessages[i]).toEqual(expectedMessages[i], "i = {}".format(i))

    def test_expect_falsy_values_to_be_false_succeeds(self):
        values = (False, 0, ())
        for value in values:
            Expect(value).toBeFalse()

    def test_expect_true_prepends_usermessage_to_assertion(self):
        try:
            Expect(False).toBeTrue("user message")
        except AssertionError as ex:
            Expect(ex.args[0]).toEqual("user message: Expected False to be True")

    def test_expect_false_prepends_usermessage_to_assertion(self):
        try:
            Expect(True).toBeFalse("user message")
        except AssertionError as ex:
            Expect(ex.args[0]).toEqual("user message: Expected True to be False")

    def test_expecting_None_toBeNone_passes(self):
        Expect(None).toBeNone()

    def test_expecting_False_toBeNone_fails(self):
        message = ""
        try:
            Expect(False).toBeNone()
        except AssertionError as ex:
            message = ex.args[0];
        
        Expect(message).toEqual("Expected False to be None")

    def test_expect_toBeNone_prepends_user_message(self):
        message = ""
        try:
            Expect(False).toBeNone("user message")
        except AssertionError as ex:
            message = ex.args[0]
        Expect(message).toEqual("user message: Expected False to be None")

    def test_expect_x_to_be_in_y_passes_when_x_is_in_y(self):
        x = 602
        y = [601, x, 603]
        Expect(x).toBeIn(y)

    def test_expect_x_to_be_in_y_passes_when_item_equal_to_x_in_y(self):
        # use numbers > 256 because of python internal behavior:
        # all numbers < 255 are declared in the machine runtime and are always
        # the same as each other. So x = 1; y = 1; least to x is y being true

        # We don't want that in this test (otherwise we'd be duplicating tests
        # so we pick larger inteers to do this with
        x = 602
        y = [601, 602, 603]
        Expect(x).toBeIn(y)

    def test_expect_x_to_be_in_y_raises_AssertionError_when_x_not_in_y(self):
        x = 602
        y = [601, 603, 605]
        message = ""
        try:
            Expect(x).toBeIn(y)
        except AssertionError as ex:
            message = ex.args[0]
        Expect(message).toEqual("Expected 602 to be in [601, 603, 605]")

    def test_expect_x_to_be_in_y_prepends_usermessage_when_condition_fails(self):
        x = 602
        y = [601, 603, 605]
        message = ""
        try:
            Expect(x).toBeIn(y, "user message")
        except AssertionError as ex:
            message = ex.args[0]
        Expect(message).toEqual("user message: Expected 602 to be in [601, 603, 605]")

    def expect_y_to_contain_x_passes_when_x_in_y(self):
        x = 602
        y = [601, x, 603]
        Expect(y).toContain(x)

    def expect_y_to_contain_x_passes_when_item_equal_to_x_in_y(self):
        x = 602
        y = [601, 602, 603]
        Expect(y).toContain(x)

    def test_expect_y_to_contain_x_fails_when_x_not_in_y(self):
        x = 602
        y = [601, 603, 605]
        message = ""
        try:
            Expect(y).toContain(x)
        except AssertionError as ex:
            message = ex.args[0]
        Expect(message).toEqual("Expected [601, 603, 605] to contain 602")    

    def test_expect_y_to_contain_x_prepends_usermessage_to_message(self):
        x = 602
        y = [601, 603, 605]
        message = ""
        try:
            Expect(y).toContain(x, "user message")
        except AssertionError as ex:
            message = ex.args[0]
        Expect(message).toEqual("user message: Expected [601, 603, 605] to contain 602")

if __name__ == "__main__":
    suite = ExpectTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())

