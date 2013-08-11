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

from collections import *

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

    def test_equals_raises_with_right_message_if_integer_items_not_equal(self):
        expect(lambda: expect(1).toEqual(2)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 to equal 2")

    def test_equals_raises_with_right_message_if_float_items_not_equal(self):
        expect(lambda: expect(1.0).toEqual(2.0)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1.0 to equal 2.0 within relative tolerance of 1e-08")

    def test_equals_compares_float_to_int_with_tolerance(self):
        expect(lambda: expect(1.0).toEqual(2)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1.0 to equal 2 within relative tolerance of 1e-08")

    def test_equals_compares_int_to_float_with_tolerance(self):
        expect(lambda: expect(1).toEqual(2.0)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 to equal 2.0 within relative tolerance of 1e-08")

    def test_equals_message_prepended_to_assert_message(self):
        expect(lambda: expect(1).toEqual(2, "user message")).toRaise(
                AssertionError,
                expectedMessageMatches = "^user message")

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
        butNoneWas = ", but none was"
        expect(message[-len(butNoneWas):]).toEqual(butNoneWas)    

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
        userMessage = "user message"
        try:
            expect(lambda: None).toRaise(KeyError, userMessage)
        except AssertionError as ex:
            message = ex.args[0]
        expect(len(message)).toBeGreaterThan(len(userMessage))
        expect(message[0:len(userMessage) + 2]).toEqual("user message: ")

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

    def test_greaterthan_prepends_usermessage_to_message(self):
        expect(lambda:
                   expect(1).toBeGreaterThan(2, "user message")).toRaise(
        AssertionError,
        expectedMessageMatches = "^user message")

    def test_expect_1_greater_than_or_equal_to_0_passes(self):
        expect(1).toBeGreaterThanOrEqualTo(0)    

    def test_expect_1_point_0_greater_than_or_Equal_to_0_passes(self):
        expect(1.0).toBeGreaterThanOrEqualTo(0)

    def test_expect_1_greater_than_or_equal_to_1_passes(self):
        expect(1).toBeGreaterThanOrEqualTo(1)

    def test_expect_1_greater_than_or_equal_to_2_fails(self):
        expect(lambda:
                   expect(1).toBeGreaterThanOrEqualTo(2)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 to be greater than or equal to 2")

    def test_expect_greater_than_or_equal_to_prepends_userMessage_to_message(self):
        expect(lambda:
                   expect(1).toBeGreaterThanOrEqualTo(2, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_0_less_than_1_passes(self):
        expect(0).toBeLessThan(1)    

    def test_expect_0_point_0_less_than_1_passes(self):
        expect(0.0).toBeLessThan(1)

    def test_expect_1_less_than_1_fails(self):
        expect(lambda:
                   expect(1).toBeLessThan(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 to be less than 1")

    def test_expect_2_less_than_1_fails(self):
        expect(lambda:
                   expect(2).toBeLessThan(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 2 to be less than 1")

    def test_lessthan_prepends_usermessage_to_message(self):
        expect(lambda:
                   expect(2).toBeLessThan(1, "user message")).toRaise(
        AssertionError,
        expectedMessageMatches = "^user message")

    def test_expect_1_less_than_or_equal_to_0_passes(self):
        expect(0).toBeLessThanOrEqualTo(1)    

    def test_expect_0_point_0_less_than_or_Equal_to_1_passes(self):
        expect(0.0).toBeLessThanOrEqualTo(1)

    def test_expect_1_less_than_or_equal_to_1_passes(self):
        expect(1).toBeLessThanOrEqualTo(1)

    def test_expect_2_less_than_or_equal_to_1_fails(self):
        expect(lambda:
                   expect(2).toBeLessThanOrEqualTo(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 2 to be less than or equal to 1")

    def test_expect_less_than_or_equal_to_prepends_userMessage_to_message(self):
        expect(lambda:
                   expect(2).toBeLessThanOrEqualTo(1, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_two_numbers_within_epsilon_are_equal(self):
        expect(1).toEqual(1+1e-10)

    def test_epsilon_does_not_equal_2_times_epsilon(self):
        expect(lambda: expect(1e-10).toEqual(2e-10)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1e-10 to equal 2e-10 within relative tolerance of 1e-08")

    def test_equality_tolerance_can_be_set(self):
        expect(1).toEqual(1.1, tolerance=1)

    def test_equality_tolernace_can_be_absolute(self):
        expect(1e-10).toEqual(2e-10, toleranceType="absolute", tolerance=1e-8)

    def test_0_equals_0_with_absolute_tolernace(self):
        expect(0).toEqual(0, toleranceType="absolute")

    def test_0_equals_0_with_relative_tolerance(self):
        expect(0).toEqual(0)

    def test_expect_0_to_be_superset_of_empty_passes(self):
        expect([1]).toBeASupersetOf(())

    def test_expect_01_to_be_superset_of_0_and_superset_of_1(self):
        expect([0, 1]).toBeASupersetOf([0])
        expect([0, 1]).toBeASupersetOf([1])

    def test_expect_0_to_be_a_superset_of_1_fails(self):
        expect(lambda: expect([0]).toBeASupersetOf(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected [0] to be a superset of 1")

    def test_expect_00_to_be_a_superset_of_empty_passes(self):
        expect([0, 0]).toBeASupersetOf(())

    def test_expect_0_to_be_a_superset_of_00_passes(self):
        expect([0, 0]).toBeASupersetOf([0])

    def test_toBeASuperset_prepends_userMessage(self):
        expect(lambda: expect([0]).toBeASupersetOf(1, "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage: ")

    def test_expect_empty_list_to_be_a_subset_of_1_passes(self):
        expect([]).toBeASubsetOf([1])

    def test_expect_0_and_1_to_be_subsets_of_01_pass(self):
        expect([0]).toBeASubsetOf([0, 1])
        expect([1]).toBeASubsetOf([0, 1])

    def test_expect_0_to_be_a_subset_of_1_fails(self):
        expect(lambda: expect([0]).toBeASubsetOf([1])).toRaise(
            AssertionError,
            expectedMessage = "Expected [0] to be a subset of [1]")

    def test_toBeASubset_prepends_userMessage(self):
        expect(lambda: expect([0]).toBeASubsetOf([1], "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage: ")

    def test_expect_two_empty_lists_to_be_equal_passes(self):
        expect([]).toEqual([])

    def test_expect_two_empty_tuplet_to_be_equal_passes(self):
        expect(tuple()).toEqual(tuple())

    def test_expect_two_nonempty_identical_lists_to_be_equal_passes(self):
        expect([1]).toEqual([1])

    def test_expect_two_nonempty_nonidentical_lists_of_the_same_length_to_be_equal_fails(self):
        expect(lambda:
                   expect([0]).toEqual([1])).toRaise(
            AssertionError,
            expectedMessage = """Expected [0] to equal [1]
First difference at index 0: 0 != 1""")

    def test_containers_of_unequal_length_get_length_mismatch_message(self):
        expect(lambda: expect([0]).toEqual([])).toRaise(
            AssertionError,
            expectedMessage = "Expected [0] to be a container of length 0")

    def test_expect_container_equals_prepends_user_message_when_containers_equal_length(self):
        expect(lambda:
                   expect([0]).toEqual([1], "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_expect_container_equals_prepends_user_message_when_containers_unequal_length(self):
        expect(lambda:
                   expect([0]).toEqual([], "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")
        
    def test_tuple_comparse_to_equivalent_list(self):
        expect((1, 2)).toEqual([1, 2])

    def test_dictionary_contains_key_passes_when_key_in_dictionary(self):
        data = { 'a' : 1 }
        expect(data).toContainKey('a')

    def test_dictionary_contains_key_fails_when_key_not_in_dictionary(self):
        data = {'a' : 1}
        expect(lambda: expect(data).toContainKey('b')).toRaise(
            AssertionError,
            expectedMessage = "Expected {'a': 1} to contain key 'b'")

    def test_dictionary_contains_key_fails_when_expected_value_but_not_key(self):
        data = {'a': 1}
        expect(lambda: expect(data).toContainKey(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected {'a': 1} to contain key 1")
                   
    def test_dictionary_contains_key_prepends_userMessage(self):
        data = {'a': 1}
        expect(lambda: expect(data).toContainKey("b", "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_default_dictionary_contains_key_passes_and_fails_as_dict(self):
        data = defaultdict(list)
        data['a'] = 1
        expect(data).toContainKey('a')

    def test_dictionary_contains_value_passes_when_value_in_dict(self):
        data = {'a': 1}
        expect(data).toContainValue(1)

    def test_dictionary_contains_value_fails_when_value_not_in_dict(self):
        data = {'a': 1}
        expect(lambda: expect(data).toContainValue(2)).toRaise(
            AssertionError,
            expectedMessage = "Expected {'a': 1} to contain value 2")

    def test_dictionary_contains_value_prepends_userMessage(self):
        data = {'a': 1}
        expect(lambda: expect(data).toContainValue(2, "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_dictionary_equal_fails_if_number_of_items_is_different(self):
        data = {'a': 1}
        expect(lambda: expect(data).toEqual({})).toRaise(
            AssertionError,
            expectedMessage = "Expected {'a': 1} to be a dictionary containing 0 items")

    def test_dictionary_equal_fails_if_keys_are_equal_in_number_and_one_key_differs(self):
        data = {'a': 1}
        expect(lambda: expect(data).toEqual({'b': 1})).toRaise(
            AssertionError,
            expectedMessage = "Expected {'a': 1} to equal {'b': 1}\nFirst missing key is 'a'")
        
    def test_dictionary_equal_fails_if_value_differs_under_same_key(self):
        data = {'a': 1}
        expect(lambda: expect(data).toEqual({'a': 2})).toRaise(
            AssertionError,
            expectedMessage = "Expected {'a': 1} to equal {'a': 2}\nFirst difference at key 'a': Expected 1 to equal 2")

    def test_dictionary_equal_passes_if_dictionaries_are_equal(self):
        data = {'a': 1}
        expect(data).toEqual({'a': 1})

    def test_dictionary_equal_prepends_userMessage_to_allMessageTypes(self):
        data = {'a': 1}
        expect(lambda: expect(data).toEqual({}, "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches= "^userMessage")
        expect(lambda: expect(data).toEqual({'b': 1}, "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches= "^userMessage")
        expect(lambda: expect(data).toEqual({'a': 2}, "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches= "^userMessage")

    def test_string_starts_with_passes_on_identical_short_strings(self):
        data = 'asdf'
        expect(data).toStartWith('asdf')

    def test_string_starts_with_passes_when_actual_starts_with_shorter_expected_start(self):
        data = 'asdf'
        expect(data).toStartWith('as')

    def test_string_starts_with_fails_if_expected_start_longer_than_actual(self):
        data = 'asdf'
        expect(lambda: expect(data).toStartWith('asdfeee')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' to be a string starting with 'asdfeee', but it was too short")

    def test_string_starts_with_fails_if_expected_start_not_matched(self):
        data = 'asdf'
        expect(lambda: expect(data).toStartWith('zzz')).toRaise(
            AssertionError,
            expectedMessage = """Expected 'asdf' to be a string starting with 'zzz'
Difference is:
- asdf
+ zzz""")

    def test_string_starts_with_prepends_userMessage_on_failure(self):
        data = 'asdf'
        expect(lambda: expect(data).toStartWith('asdfeee', 'userMessage')).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_string_ends_with_passes_on_identical_short_strings(self):
        data = 'asdf'
        expect(data).toEndWith('asdf')

    def test_string_ends_with_passes_when_actual_ends_with_shorter_expected_end(self):
        data = 'asdf'
        expect(data).toEndWith('df')

    def test_string_ends_with_fails_if_expected_end_longer_than_actual(self):
        data = 'asdf'
        expect(lambda: expect(data).toEndWith('eeeasdf')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' to be a string ending with 'eeeasdf', but it was too short")

    def test_string_ends_with_fails_if_expected_end_not_matched(self):
        data = 'asdf'
        expect(lambda: expect(data).toEndWith('zzz')).toRaise(
            AssertionError,
            expectedMessage = """Expected 'asdf' to be a string ending with 'zzz'
Difference is:
- asdf
+ zzz""")

    def test_string_starts_with_prepends_userMessage_on_failure(self):
        data = 'asdf'
        expect(lambda: expect(data).toEndWith('eeeasdf', 'userMessage')).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_string_contains_passes_on_identical_strings(self):
        actual = 'asdf'
        expect(actual).toContain('asdf')

    def test_string_contains_passes_when_data_starts_with_expected(self):
        actual = 'asdf'
        expect(actual).toContain('as')

    def test_string_contains_passes_when_actual_ends_with_expected(self):
        actual = 'asdf'
        expect(actual).toContain('df')

    def test_string_contains_passes_when_expected_embedded_in_actual(self):
        actual = 'asdf'
        expect(actual).toContain('sd')

    def test_string_contains_fails_When_expected_not_in_actual(self):
        actual = 'asdf'
        expect(lambda: expect(actual).toContain('zzz')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' to be a string containing 'zzz'")

    def test_string_contains_prepends_userMessage(self):
        actual = 'asdf'
        expect(lambda: expect(actual).toContain('zzz', 'userMessage')).toRaise(
            AssertionError,
            expectedMessageMatches = '^userMessage')

    def test_string_equals_doesnt_raise_if_string_items_are_equal(self):
        expect("hello").toEqual("hello")

    def test_string_equals_raises_with_right_message_if_string_items_not_equal(self):
        expect(lambda: expect("hello").toEqual("world")).toRaise(
            AssertionError,
            expectedMessage = """Expected 'hello' to equal 'world'
Difference is:
- hello
+ world""")

    def test_string_equals_prepends_userMessage_on_failure(self):
        expect(lambda: expect('hello').toEqual('world', 'userMessage')).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")
        

    def test_expecting_string1_to_equal_double1_fails(self):
        expect(lambda: expect("1").toEqual(1)).toRaise(
            AssertionError,
            expectedMessage = "Cannot compare instance of <class 'str'> to "
            "instance of <class 'int'> because their types differ")
        

        

if __name__ == "__main__":
    suite = ExpectTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())


