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

class NumericExpectationsTests(TestCase):

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
        expect(lambda: withUserMessage("user message").expect(1).toEqual(2)).toRaise(
                AssertionError,
                expectedMessageMatches = "^user message")

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
                   withUserMessage("userMessage").expect(1).toBeGreaterThan(2)).toRaise(
        AssertionError,
        expectedMessageMatches = "^userMessage")

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
                   withUserMessage("userMessage").expect(1).toBeGreaterThanOrEqualTo(2)).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

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
                   withUserMessage("userMessage").expect(2).toBeLessThan(1)).toRaise(
        AssertionError,
        expectedMessageMatches = "^userMessage")

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
                   withUserMessage("userMessage").expect(2).toBeLessThanOrEqualTo(1)).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

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

class NumericNotExpectationsTests(TestCase):

    def test_equals_doesnt_raise_if_numbers_unequal(self):
        expect(1).Not.toEqual(2)
        # Pass condition if we get here with no exception

    def test_equals_raises_correctly_if_integers_equal(self):
        expect(lambda: expect(1).Not.toEqual(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 not to equal 1")

    def test_equals_raised_correctly_if_floats_equal(self):
        expect(lambda: expect(1.0).Not.toEqual(1.0)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1.0 not to equal 1.0 within relative tolerance of 1e-08")

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
               withUserMessage("userMessage").expect(1).Not.toBeGreaterThan(0)).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_expect_1_not_greater_than_or_equal_to_2_passes(self):
        expect(1).Not.toBeGreaterThanOrEqualTo(2)

    def test_expect_1_not_greater_than_or_equal_to_1_fails(self):
        expect(lambda:
                   expect(1).Not.toBeGreaterThanOrEqualTo(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 not to be greater than or equal to 1")

    def test_expect_not_greater_than_or_equal_prepends_userMessae_to_message(self):
        expect(lambda:
                   withUserMessage("userMessage").expect(1).Not.toBeGreaterThanOrEqualTo(1)).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

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
               withUserMessage("userMessage").expect(0).Not.toBeLessThan(1)).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_expect_2_not_less_than_or_equal_to_1_passes(self):
        expect(2).Not.toBeLessThanOrEqualTo(1)

    def test_expect_1_not_less_than_or_equal_to_1_fails(self):
        expect(lambda:
                   expect(1).Not.toBeLessThanOrEqualTo(1)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 not to be less than or equal to 1")

    def test_expect_not_less_than_or_equal_prepends_userMessage_to_message(self):
        expect(lambda:
                   withUserMessage("userMessage").expect(1).Not.toBeLessThanOrEqualTo(1)).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")
