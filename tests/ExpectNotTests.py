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

def raise_error():
    raise KeyError("The wrong key was presented")


class ExpectNotTests(TestCase):
    
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_fail_doesnt_raise_anything(self):
        expect(True).Not.fail()
        # pass condition should be that we get to this point

    def test_success_raises_AssertionError(self):
        expect(lambda: expect(True).Not.success("Message")).toRaise(
                AssertionError,
                expectedMessage = "Message")

    def test_equals_doesnt_raise_if_numbers_unequal(self):
        expect(1).Not.toEqual(2)
        # Pass condition if we get here with no exception

    def test_equals_raises_correctly_if_numbers_equal(self):
        expect(lambda: expect(1).Not.toEqual(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 not to equal 1 within relative tolerance of 1e-08")

    def test_equals_doesnt_raise_if_two_strings_unequal(self):
        expect("asdf").Not.toEqual("zxc")

    def test_equals_raises_correctly_if_strings_equal(self):
        expect(lambda: expect("asdf").Not.toEqual("asdf")).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to equal 'asdf'")

    def test_expecting_string1_not_to_equal_double1_fails(self):
        expect(lambda: expect("1").Not.toEqual(1)).toRaise(
            AssertionError,
            expectedMessage = ("Cannot compare instance of <class 'str'> to "
                               "instance of <class 'int'> because their types differ"))

    def test_expect_truthy_values_not_to_be_true_fails(self):
        values = (True, 1, (1))
        expectedMessages = ("Expected True not to be True",
                          "Expected 1 not to be True", 
                          "Expected (1) not to be True")
        for i in range(0, len(expectedMessages) - 1):
            userMessage = "Index {}".format(i)
            expect(lambda: expect(values[i]).Not.toBeTrue()).toRaise(
                AssertionError,
                userMessage = userMessage,
                expectedMessage = expectedMessages[i])

    def test_expect_falsy_values_not_to_be_true_succeeds(self):
        values = (False, 0, ())
        for value in values:
            expect(value).Not.toBeTrue()

    def test_expect_truthy_values_not_to_be_false_succeeds(self):
        values = (True, 1, (1))
        for value in values:
            expect(value).Not.toBeFalse()

    def test_expect_falsy_values_not_to_be_false_fails(self):
        values = (False, 0, ())
        expectedMessages = ("Expected False not to be False",
                          "Expected 0 not to be False", 
                          "Expected () not to be False")
        for i in range(1, len(values) - 1):
            expect(lambda: expect(values[i]).Not.toBeFalse()).toRaise(
                AssertionError,
                userMessage = "Index {}".format(i),
                expectedMessage = expectedMessages[i])

    def test_expect_not_true_prepends_usermessage_to_assertion(self):
        expect(lambda: expect(True).Not.toBeTrue("user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_not_false_prepends_usermessage_to_assertion(self):
        expect(lambda: expect(False).Not.toBeFalse("user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_not_False_toBeNone_passes(self):
        expect(False).Not.toBeNone()

    def test_expect_not_None_toBeNone_fails_with_correct_message(self):
        expect(lambda: expect(None).Not.toBeNone()).toRaise(
            AssertionError,
            expectedMessage = "Expected None not to be None")

    def test_expect_not_toBeNone_prepends_userMessage(self):
        expect(lambda: expect(None).Not.toBeNone("user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_not_x_to_be_in_y_passes_when_x_is_not_in_y(self):
        x = 602
        y = [601, 603, 605]
        expect(x).Not.toBeIn(y)

    def test_expect_not_x_to_be_in_y_raises_AssertionError_when_x_in_y(self):
        x = 602
        y = [601, x, 603]
        expect(lambda: expect(x).Not.toBeIn(y)).toRaise(
            AssertionError,
            expectedMessage = "Expected 602 not to be in [601, 602, 603]")

    def test_expect_not_x_to_be_in_y_raises_AssertionError_when_item_equal_to_x_in_y(self):
        x = 602
        y = [601, 602, 603]
        expect(lambda: expect(x).Not.toBeIn(y)).toRaise(
            AssertionError,
            expectedMessage = "Expected 602 not to be in [601, 602, 603]")
    
    def test_expect_not_x_to_be_in_y_prepends_usermessage_on_failure(self):
        x = 602
        y = [601, 602, 603]
        expect(lambda: expect(x).Not.toBeIn(y, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_not_y_to_contain_x_passes_when_x_not_in_y(self):
        x = 602
        y = [601, 603, 605]
        expect(y).Not.toContain(x)

    def test_expect_not_y_to_contain_x_fails_when_x_in_y(self):
        x = 602
        y = [601, 602, 603]
        expect(lambda: expect(y).Not.toContain(x)).toRaise(
            AssertionError,
            expectedMessage = "Expected [601, 602, 603] not to contain 602")
        
    def test_expect_not_y_to_contain_x_prepends_usermessage(self):
        x = 602
        y = [601, 602, 603]
        expect(lambda: expect(y).Not.toContain(x, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")
        
    def test_expect_not_1_instanceof_float_passes(self):
        # TODO: this should be expectNot
        expect(1).Not.toBeAnInstanceOf(float)

    def test_expect_not_1_instanceof_int_fails(self):
        expect(lambda: expect(1).Not.toBeAnInstanceOf(int)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 not to be an instance of <class 'int'>"
            " but was an instance of <class 'int'>")

    def test_expect_not_self_instanceof_TestResults_passes(self):
        expect(self).Not.toBeAnInstanceOf(TestResults)

    def test_expect_not_self_instanceof_ExpectNotTests_fails(self):
        expect(lambda: expect(self).Not.toBeAnInstanceOf(ExpectNotTests)).toRaise(
            AssertionError,
            expectedMessage = "Expected <ExpectNotTests.ExpectNotTests object> "
            "not to be an instance of <class 'ExpectNotTests.ExpectNotTests'> "
            "but was an instance of <class 'ExpectNotTests.ExpectNotTests'>")

    def test_expect_not_self_instanceof_TestCase_fails(self):
        expect(lambda: expect(self).Not.toBeAnInstanceOf(TestCase)).toRaise(
            AssertionError,
            expectedMessage = "Expected <ExpectNotTests.ExpectNotTests object>"
            " not to be an instance of <class 'WellBehavedPython.TestCase.TestCase'>"
            " but was an instance of <class 'ExpectNotTests.ExpectNotTests'>")        

    def test_instance_of_prepends_usermessage(self):
        expect(lambda: expect(1).Not.toBeAnInstanceOf(
                int, 
                "user message")).toRaise(
                AssertionError,
                expectedMessageMatches = "^user message")

    def test_expect_not_exception_raised_passes_if_exception_not_raised(self):
        expect(lambda: None).Not.toRaise(Exception)

    def test_expect_not_exception_fails_if_exact_exception_raised(self):
        message = ""
        try:
            expect(raise_error).Not.toRaise(KeyError)
        except AssertionError as ex:
            message = ex.args[0]
            
        expect(message).toEqual("Expected <function raise_error> "
            "not to raise an instance of <class 'KeyError'>"
            ", but it raised an instance of <class 'KeyError'>")

    def test_expect_not_exception_prepends_usermessage_when_exact_exception_raised(self):
        message = ""
        try:
            expect(raise_error).Not.toRaise(KeyError, "user message")
        except AssertionError as ex:
            message = ex.args[0]

        expect(message).toEqual("user message: "
                                "Expected <function raise_error>"
                                " not to raise an instance of <class 'KeyError'>"
                                ", but it raised an instance of <class 'KeyError'>")

    def test_expected_exception_with_unexpected_message_passes(self):
        expect(raise_error).Not.toRaise(KeyError, expectedMessage = "This is not the right message")

    def test_expected_exception_with_expected_message_fails(self):
        message = ""
        try:
            expect(raise_error).Not.toRaise(KeyError, expectedMessage = "The wrong key was presented")
        except AssertionError as ex:
            message = ex.args[0]

        expect(message).toEqual("Expected <function raise_error>"
                                " not to raise an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'"
                                ", but it raised an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'")

    def test_expect_not_exception_with_message_not_matching_regexp_passes(self):
        expect(raise_error).Not.toRaise(KeyError, expectedMessageMatches = "^not")

    def test_expect_not_raises_fails_if_error_matches_and_message_matches_regexp(self):
        message = ""
        try:
            expect(raise_error).Not.toRaise(KeyError, expectedMessageMatches = ".*")
        except AssertionError as ex:
            message = ex.args[0]

        expect(message).toEqual("Expected <function raise_error>"
                                " not to raise an instance of <class 'KeyError'>"
                                " with message matching regular expression '.*'"
                                ", but it raised an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'")

    def test_expect_1_not_greater_than_1_passes(self):
        expect(1).Not.toBeGreaterThan(1)

    def test_expect_1_not_greater_than_2_passes(self):
        expect(1).Not.toBeGreaterThan(2)        

    def test_expect_1_not_greater_than_0_fails(self):
        expect(lambda: 
               expect(1).Not.toBeGreaterThan(0)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 not to be greater than 0")

    def test_not_greater_than_prepends_usermessage_to_message(self):
        expect(lambda: 
               expect(1).Not.toBeGreaterThan(0, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_1_not_greater_than_or_equal_to_2_passes(self):
        expect(1).Not.toBeGreaterThanOrEqualTo(2)

    def test_expect_1_not_greater_than_or_equal_to_1_fails(self):
        expect(lambda:
                   expect(1).Not.toBeGreaterThanOrEqualTo(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 not to be greater than or equal to 1")

    def test_expect_not_greater_than_or_equal_prepends_userMessae_to_message(self):
        expect(lambda:
                   expect(1).Not.toBeGreaterThanOrEqualTo(1, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_1_not_less_than_1_passes(self):
        expect(1).Not.toBeLessThan(1)

    def test_expect_2_not_less_than_1_passes(self):
        expect(2).Not.toBeLessThan(1)        

    def test_expect_0_not_less_than_1_fails(self):
        expect(lambda: 
               expect(0).Not.toBeLessThan(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 0 not to be less than 1")

    def test_not_less_than_prepends_usermessage_to_message(self):
        expect(lambda: 
               expect(0).Not.toBeLessThan(1, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_2_not_less_than_or_equal_to_1_passes(self):
        expect(2).Not.toBeLessThanOrEqualTo(1)

    def test_expect_1_not_less_than_or_equal_to_1_fails(self):
        expect(lambda:
                   expect(1).Not.toBeLessThanOrEqualTo(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 not to be less than or equal to 1")

    def test_expect_not_less_than_or_equal_prepends_userMessage_to_message(self):
        expect(lambda:
                   expect(1).Not.toBeLessThanOrEqualTo(1, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_0_not_to_be_a_superset_of_empty_fails(self):
        expect(lambda: expect([1]).Not.toBeASupersetOf(())).toRaise(
            AssertionError,
            expectedMessage = "Expected [1] not to be a superset of ()")

    def test_expect_01_to_be_superset_of_0_and_superset_of_1(self):
        expect(lambda: expect([0, 1]).Not.toBeASupersetOf([0])).toRaise(
            AssertionError,
            expectedMessage = "Expected [0, 1] not to be a superset of [0]")
        expect(lambda: expect([0, 1]).Not.toBeASupersetOf([1])).toRaise(
            AssertionError,
            expectedMessage = "Expected [0, 1] not to be a superset of [1]")

    def test_expect_0_to_be_a_superset_of_1_fails(self):
        expect([0]).Not.toBeASupersetOf(1)

    def test_toBeASuperset_prepends_userMessage(self):
        expect(lambda: expect([0, 1]).Not.toBeASupersetOf([0], "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage: ")

    def test_0_not_toBeASubset_of_empty_passes(self):
        expect([0]).Not.toBeASubsetOf([])

    def test_0_not_to_beASubset_of_01_fails(self):
        expect(lambda: expect([0]).Not.toBeASubsetOf([0, 1])).toRaise(
                AssertionError,
                expectedMessage = "Expected [0] not to be a subset of [0, 1]")

    def test_not_to_beASubset_prepends_userMessage(self):
        expect(lambda: expect([0]).Not.toBeASubsetOf([0, 1], "userMessage")).toRaise(
                AssertionError,
                expectedMessageMatches = "^userMessage: ")


    def test_dictionary_not_contains_key_fails_when_key_in_dictionary(self):
        data = { 'a' : 1 }
        expect(lambda: expect(data).Not.toContainKey('a')).toRaise(
            AssertionError,
            expectedMessage = "Expected {'a': 1} not to contain key 'a'")

    def test_dictionary_not_contains_key_passes_when_key_not_in_dictionary(self):
        data = {'a': 1}
        expect(data).Not.toContainKey('b')

    def test_dictionary_not_contains_key_prepends_userMessage(self):
        data = { 'a' : 1 }
        expect(lambda: expect(data).Not.toContainKey("a", "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches= "^userMessage: ")

    def test_dictionary_not_contains_value_passes_when_value_not_in_dictionary(self):
        data = { 'a': 1 }
        expect(data).Not.toContainValue(2)

    def test_dictionary_not_contains_value_fails_when_value_in_dictionary(self):
        data = { 'a': 1 }
        expect(lambda: expect(data).Not.toContainValue(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected {'a': 1} not to contain value 1")
        



if __name__ == "__main__":
    suite = ExpectNotTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())


