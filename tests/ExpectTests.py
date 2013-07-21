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
from WellBehavedPython.api import *

import re

def raise_error():
    raise KeyError("The wrong key was presented")

class ExpectTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_expects_fail_throws_AssertionError(self):
        # DON'T USE EXPECTED EXCEPTION
        # The test for fail is so fundamental, that it has to be
        # performed with tests outside the framework itself
        # 
        # Otherwise, we're assuming fail works while testing the
        # exceptino based behavior of fail. The test for the 
        # expected message is different, as that is testing the
        # message structure, and not the fundamental pass/fail
        # behavior.
        raised = True
        try:
            expect(True).fail()
            raised = False
        except AssertionError:
            pass
        
        # Fail is so fundamental that we don't bootstrap
        # the asertion with Expect.toBeTrue() as that uses fail
        assert raised, "Expected an AssertionError to have been thrown"

    def test_failure_stores_message_if_provided(self):
        expect(lambda: expect(True).fail("ExpectedMessage")).toRaise(
            AssertionError,
            expectedMessage = "ExpectedMessage")
        
    def test_equals_doesnt_raise_if_numeric_items_are_equal(self):
        expect(1).toEqual(1)

    def test_equals_raises_with_right_message_if_numeric_items_not_equal(self):
        expect(lambda: expect(1).toEqual(2)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 to equal 2")

    def test_equals_message_prepended_to_assert_message(self):
        expect(lambda: expect(1).toEqual(2, "user message")).toRaise(
                AssertionError,
                expectedMessageMatches = "^user message")

    def test_equals_doesnt_raise_if_string_items_are_equal(self):
        expect("hello").toEqual("hello")

    def test_equals_raises_with_right_message_if_string_items_not_equal(self):
        expect(lambda: expect("hello").toEqual("world")).toRaise(
            AssertionError,
            expectedMessage = "Expected 'hello' to equal 'world'")

    def test_expecting_string1_to_equal_double1_fails(self):
        expect(lambda: expect("1").toEqual(1)).toRaise(
            AssertionError,
            expectedMessage = "Cannot compare instance of <class 'str'> to "
            "instance of <class 'int'> because their types differ")
        

    def test_expect_truthy_values_to_be_true_succeeds(self):
        expect(True).toBeTrue()
        expect(1).toBeTrue()
        expect((1)).toBeTrue()

    def test_expect_falsy_values_to_be_true_fails(self):
        values = (False, 0, ())
        expectedMessages = ("Expected False to be True", 
                            "Expected 0 to be True",
                            "Expected () to be True")
        for i in range(0, len(values) - 1):
            expect(lambda: expect(values[i]).toBeTrue()).toRaise(
                AssertionError,
                expectedMessage = expectedMessages[i])

    def test_expect_truthy_values_to_be_false_fails(self):
        values = (True, 1, (1))
        expectedMessages = ("Expected True to be False",
                            "Expected 1 to be False",
                            "Expected (1) to be False")

        for i in range(0, len(values) - 1):
            expect(lambda: expect(values[i]).toBeFalse()).toRaise(
                AssertionError,
                expectedMessage = expectedMessages[i])

    def test_expect_falsy_values_to_be_false_succeeds(self):
        values = (False, 0, ())
        for value in values:
            expect(value).toBeFalse()

    def test_expect_true_prepends_usermessage_to_assertion(self):
        expect(lambda: expect(False).toBeTrue("user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_false_prepends_usermessage_to_assertion(self):
        expect(lambda: expect(True).toBeFalse("user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expecting_None_toBeNone_passes(self):
        expect(None).toBeNone()

    def test_expecting_False_toBeNone_fails(self):
        expect(lambda: expect(False).toBeNone()).toRaise(
            AssertionError,
            expectedMessage = "Expected False to be None")

    def test_expect_toBeNone_prepends_user_message(self):
        expect(lambda: expect(False).toBeNone("user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_x_to_be_in_y_passes_when_x_is_in_y(self):
        x = 602
        y = [601, x, 603]
        expect(x).toBeIn(y)

    def test_expect_x_to_be_in_y_passes_when_item_equal_to_x_in_y(self):
        # use numbers > 256 because of python internal behavior:
        # all numbers < 255 are declared in the machine runtime and are always
        # the same as each other. So x = 1; y = 1; least to x is y being true

        # We don't want that in this test (otherwise we'd be duplicating tests
        # so we pick larger inteers to do this with
        x = 602
        y = [601, 602, 603]
        expect(x).toBeIn(y)

    def test_expect_x_to_be_in_y_raises_AssertionError_when_x_not_in_y(self):
        x = 602
        y = [601, 603, 605]
        expect(lambda: expect(x).toBeIn(y)).toRaise(
            AssertionError,
            expectedMessage = "Expected 602 to be in [601, 603, 605]")

    def test_expect_x_to_be_in_y_prepends_usermessage_when_condition_fails(self):
        x = 602
        y = [601, 603, 605]
        expect(lambda: expect(x).toBeIn(y, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def expect_y_to_contain_x_passes_when_x_in_y(self):
        x = 602
        y = [601, x, 603]
        expect(y).toContain(x)

    def expect_y_to_contain_x_passes_when_item_equal_to_x_in_y(self):
        x = 602
        y = [601, 602, 603]
        expect(y).toContain(x)

    def test_expect_y_to_contain_x_fails_when_x_not_in_y(self):
        x = 602
        y = [601, 603, 605]
        expect(lambda: expect(y).toContain(x)).toRaise(
            AssertionError,
            expectedMessage = "Expected [601, 603, 605] to contain 602")    

    def test_expect_y_to_contain_x_prepends_usermessage_to_message(self):
        x = 602
        y = [601, 603, 605]
        expect(lambda: expect(y).toContain(x, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_1_instanceof_int_passes(self):
        expect(1).toBeAnInstanceOf(int)

    def test_1_instanceof_float_fails(self):
        expect(lambda: expect(1).toBeAnInstanceOf(float)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 to be an instance of <class 'float'> but was an instance of <class 'int'>")

    def test_instance_of_userclass_passes(self):
        expect(TestResults()).toBeAnInstanceOf(TestResults)

    def test_instance_of_wrong_userclass_fails(self):
        expect(lambda: expect(TestResults()).toBeAnInstanceOf(TestSuite)).toRaise(
            AssertionError,
            expectedMessage = "Expected <WellBehavedPython.TestResults.TestResults object>"
            " to be an instance of <class 'WellBehavedPython.TestSuite.TestSuite'>"
            " but was an instance of <class 'WellBehavedPython.TestResults.TestResults'>")

    def test_instance_of_derived_class_matches_base_class(self):
        expect(self).toBeAnInstanceOf(TestCase)

    def test_instance_of_prepends_usermessage(self):
        expect(lambda: 
               expect(1).toBeAnInstanceOf(float, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expected_exception_passes_when_exception_matches(self):
        expect(raise_error).toRaise(KeyError)

    def test_expected_exception_passes_when_exception_is_derived_from_match(self):
        expect(raise_error).toRaise(LookupError)
        

    def test_expected_exception_fails_if_exception_not_raised(self):
        # We have to use a manual expected exception here to check that
        # expected exception raises the right exception
        message = ""
        try:
            expect(lambda: None).toRaise(Exception)
        except AssertionError as ex:
            message = ex.args[0]
        expect(message).toEqual("Expected <function <lambda>> to raise an instance of <class 'Exception'>, but none was")
    

    def test_expected_exception_fails_if_wrong_exception_raised(self):
        message = ""
        try:
            expect(raise_error).toRaise(FloatingPointError)
        except AssertionError as ex:
            message = ex.args[0]
        expect(message).toEqual("Expected <function raise_error> "
                                "to raise an instance of <class 'FloatingPointError'>, "
                                "but it raised an instance of <class 'KeyError'>")

    def test_expected_exception_prepends_usermessage_on_wrong_exception(self):
        message = ""
        try:
            expect(raise_error).toRaise(FloatingPointError, "user message")
        except AssertionError as ex:
            message = ex.args[0]
        expect(message).toEqual("user message: "
                                "Expected <function raise_error> "
                                "to raise an instance of <class 'FloatingPointError'>, "
                                "but it raised an instance of <class 'KeyError'>")

    def test_expected_exception_prepends_usermessage_on_no_exception(self):
        message = ""
        try:
            expect(lambda: None).toRaise(KeyError, "user message")
        except AssertionError as ex:
            message = ex.args[0]
        expect(message).toEqual("user message: "
                                "Expected <function <lambda>> "
                                "to raise an instance of <class 'KeyError'>"
                                ", but none was"                                )

    def test_expect_exception_with_expected_message_passes(self):
        expect(raise_error).toRaise(
            KeyError,
            expectedMessage = "The wrong key was presented")

    def test_expect_exception_with_unexpected_message_fails(self):
        message = ""
        try:
            expect(raise_error).toRaise(KeyError, expectedMessage = "This is not the right message")
        except AssertionError as ex:
            message = ex.args[0]
        
        expect(message).toEqual("Expected <function raise_error>"
                                " to raise an instance of <class 'KeyError'>"
                                " with message 'This is not the right message'"
                                ", but it raised an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'")

    def test_expected_exception_with_message_matching_regexp_passes(self):
        expect(raise_error).toRaise(KeyError, expectedMessageMatches = ".*")

    def test_expected_exception_with_message_not_matching_regexp_fails(self):
        message = ""
        try:
            expect(raise_error).toRaise(
                KeyError,
                expectedMessageMatches = "^not")
        except AssertionError as ex:
            message = ex.args[0]
            
        expect(message).toEqual("Expected <function raise_error>"
                                " to raise an instance of <class 'KeyError'>"
                                " with message matching regular expression '^not'"
                                ", but it raised an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'")

    def test_expected_exception_with_message_matching_compiled_regexp_passes(self):
        regexp = re.compile(".*")
        expect(raise_error).toRaise(KeyError, expectedMessageMatches = regexp)

    def test_expected_exception_with_message_not_matching_compiled_regexp_fails(self):
        message = ""
        regexp = re.compile("^not")
        try:
            expect(raise_error).toRaise(KeyError, expectedMessageMatches = regexp)
        except AssertionError as ex:
            message = ex.args[0]
            
        expect(message).toEqual("Expected <function raise_error>"
                                " to raise an instance of <class 'KeyError'>"
                                " with message matching regular expression '^not'"
                                ", but it raised an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'")

    def test_expect_1_greater_than_0_passes(self):
        expect(1).toBeGreaterThan(0)    

    def test_expect_1_point_0_greater_than_0_passes(self):
        expect(1.0).toBeGreaterThan(0)

    def test_expect_1_greater_than_1_fails(self):
        expect(lambda:
                   expect(1).toBeGreaterThan(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 to be greater than 1")

    def test_expect_1_greater_than_2_fails(self):
        expect(lambda:
                   expect(1).toBeGreaterThan(2)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 to be greater than 2")

if __name__ == "__main__":
    suite = ExpectTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())


