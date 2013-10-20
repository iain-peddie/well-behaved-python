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

class StringExpectationsTests(TestCase):
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

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

    def test_expect_string_to_match_regexp_passes_when_string_matches(self):
        actual = 'asdf'
        expect(actual).toMatch('a.*f')

    def test_expect_string_to_match_regexp_in_middle_passes(self):
        actual = 'asdf'
        pattern = 's.*f'
        expect(actual).toMatch(pattern)

    def test_expect_string_to_match_regexp_fails_When_string_doesnt_match(self):
        actual = 'asdf'
        pattern= '^[^asdf]+$'
        expect(lambda: expect(actual).toMatch(pattern)).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' to be a string matching regular expression pattern '^[^asdf]+$'")

    def test_expect_string_to_match_compiled_regexp_passes_when_string_matches(self):
        actual = 'asdf'
        pattern = re.compile('a.*f')
        expect(actual).toMatch(pattern)

    def test_expect_string_to_match_compiled_regexp_fails_when_string_doesnt_match(self):
        actual = 'asdf'
        pattern = re.compile('^[^asdf]+$')
        expect(lambda: expect(actual).toMatch(pattern)).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' to be a string matching regular expression pattern '^[^asdf]+$'")

    def test_expect_string_to_match_prepends_userMessage_on_failure(self):
        actual = 'asdf'
        pattern = re.compile('^[^asdf]+$')
        expect(lambda: expect(actual).toMatch(pattern, 'userMessage')).toRaise(
            AssertionError,
            expectedMessageMatches = '^userMessage')                    

class ContainerExpectationsTests(TestCase):
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)
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



