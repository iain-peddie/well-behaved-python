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
        expect(lambda: expect('hello').withUserMessage('userMessage').toEqual('world')).toRaise(
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




class StringNotExpectationsTests(TestCase):
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_string_not_to_start_with_passes_if_strings_start_differently(self):
        data = 'asdf'
        expect(data).Not.toStartWith('zzz')

    def test_string_not_to_start_with_fails_if_strings_identical(self):
        data = 'asdf'
        expect(lambda: expect(data).Not.toStartWith('asdf')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to be a string starting with 'asdf'")

    def test_string_not_to_start_With_fails_if_expected_starts_with_expected_start(self):
        data = 'asdf'
        expect(lambda: expect(data).Not.toStartWith('as')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to be a string starting with 'as'")
        
    def test_string_not_to_end_with_passes_if_strings_end_differently(self):
        data = 'asdf'
        expect(data).Not.toEndWith('zzz')

    def test_string_not_to_end_with_fails_if_strings_identical(self):
        data = 'asdf'
        expect(lambda: expect(data).Not.toEndWith('asdf')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to be a string ending with 'asdf'")

    def test_string_not_to_end_With_fails_if_expected_ends_with_expected_end(self):
        data = 'asdf'
        expect(lambda: expect(data).Not.toEndWith('df')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to be a string ending with 'df'")

    def test_string__not_contains_fails_on_identical_strings(self):
        actual = 'asdf'
        expect(lambda: expect(actual).Not.toContain('asdf')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to be a string containing 'asdf'")

    def test_string_not_contains_fails_when_data_starts_with_expected(self):
        actual = 'asdf'
        expect(lambda: expect(actual).Not.toContain('as')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to be a string containing 'as'")

    def test_string_not_contains_fails_when_actual_ends_with_expected(self):
        actual = 'asdf'
        expect(lambda: expect(actual).Not.toContain('df')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to be a string containing 'df'")

    def test_string_notcontains_fails_when_expected_embedded_in_actual(self):
        actual = 'asdf'
        expect(lambda: expect(actual).Not.toContain('sd')).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to be a string containing 'sd'")

    def test_string_not_contains_passesfails_when_expected_not_in_actual(self):
        actual = 'asdf'
        expect(actual).Not.toContain('zzz')

    def test_string_not_contains_prepends_userMessage(self):
        actual = 'asdf'
        expect(lambda: expect(actual).Not.toContain('sd', 'userMessage')).toRaise(
            AssertionError,
            expectedMessageMatches = '^userMessage')

    def test_equals_doesnt_raise_if_two_strings_unequal(self):
        actual = 'asdf'
        expect(actual).Not.toEqual("zxc")

    def test_equals_raises_correctly_if_strings_equal(self):
        actual = 'asdf'
        expect(lambda: expect(actual).Not.toEqual("asdf")).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to equal 'asdf'")

    def test_expecting_string1_not_to_equal_double1_fails(self):
        expect(lambda: expect("1").Not.toEqual(1)).toRaise(
            AssertionError,
            expectedMessage = ("Cannot compare instance of <class 'str'> to " +
                               "instance of <class 'int'> because their types differ"))


    def test_string_not_equals_prepends_userMessage_on_failure(self):
        actual = 'asdf'
        expect(lambda: expect(actual).withUserMessage('userMessage').Not.toEqual('asdf')).toRaise(
            AssertionError,
            expectedMessageMatches = '^userMessage')

    def test_string_not_matches_passes_when_string_doesnt_match_pattern(self):
        actual = 'asdf'
        pattern = 'z+'
        expect(actual).Not.toMatch(pattern)

    def test_string_not_matches_fails_when_string_matches_pattern(self):
        actual = 'asdf'
        pattern = '.*'
        expect(lambda: expect(actual).Not.toMatch(pattern)).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to be a string matching regular expression pattern '.*'")

    def test_string_not_matches_passes_when_string_doesnt_match_compiled_pattern(self):
        actual = 'asdf'
        pattern = re.compile('z+')
        expect(actual).Not.toMatch(pattern)

    def test_string_not_matches_fails_when_string_matches_compiled_pattern(self):
        actual = 'asdf'
        pattern = re.compile('.*')
        expect(lambda: expect(actual).Not.toMatch(pattern)).toRaise(
            AssertionError,
            expectedMessage = "Expected 'asdf' not to be a string matching regular expression pattern '.*'")

    def test_string_not_matches_prepends_userMessage_on_failure(self):
        actual = 'asdf'
        pattern = 'asdf'
        expect(lambda: expect(actual).Not.toMatch(pattern, 'userMessage')).toRaise(
            AssertionError,
            expectedMessageMatches = '^userMessage')

