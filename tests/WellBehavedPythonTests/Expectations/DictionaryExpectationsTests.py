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

from WellBehavedPython.api import *
from WellBehavedPython.Engine.TestCase import *

from collections import *

class DictionaryExpectationsTests(TestCase):

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
        expect(lambda: withUserMessage("userMessage").expect(data).toContainKey("b")).toRaise(
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
        expect(lambda: withUserMessage("userMessage").expect(data).toContainValue(2)).toRaise(
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
        expect(lambda: withUserMessage("userMessage").expect(data).toEqual({})).toRaise(
            AssertionError,
            expectedMessageMatches= "^userMessage")
        expect(lambda: withUserMessage("userMessage").expect(data).toEqual({'b': 1})).toRaise(
            AssertionError,
            expectedMessageMatches= "^userMessage")
        expect(lambda: withUserMessage("userMessage").expect(data).toEqual({'a': 2})).toRaise(
            AssertionError,
            expectedMessageMatches= "^userMessage")

class DictionaryNotExpectationsTests(TestCase):

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
        expect(lambda: withUserMessage("userMessage").expect(data).Not.toContainKey("a")).toRaise(
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

    def test_dictionary_not_contains_value_fails_when_value_in_dictionary(self):
        data = { 'a': 1 }
        expect(lambda: withUserMessage("userMessage").expect(data).Not.toContainValue(1)).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")
        
    def test_dictionary_not_equal_passes_if_number_of_items_is_different(self):
        data = {'a': 1}
        expect(data).Not.toEqual({})

    def test_dictionary_not_equal_passes_if_keys_are_equal_in_number_and_one_key_differs(self):
        data = {'a': 1}
        expect(data).Not.toEqual({'b': 1})
        
    def test_dictionary_not_equal_passes_if_value_differs_under_same_key(self):
        data = {'a': 1}
        expect(data).Not.toEqual({'a': 2})

    def test_dictionary_not_equal_fails_if_dictionaries_are_equal(self):
        data = {'a': 1}
        expect(lambda: expect(data).Not.toEqual({'a': 1})).toRaise(
            AssertionError,
            expectedMessage = "Expected {'a': 1} not to equal {'a': 1}")

    def test_dictionary_not_equal_prepends_userMessage_on_failure(self):
        data = {'a': 1}
        expect(lambda: withUserMessage("userMessage").expect(data).Not.toEqual({'a': 1})).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

