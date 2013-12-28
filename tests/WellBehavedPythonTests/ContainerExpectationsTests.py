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
        expect(lambda: expect([0]).withUserMessage("userMessage").toBeASupersetOf(1)).toRaise(
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
                   expect([0]).withUserMessage("userMessage").toEqual([1])).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_expect_container_equals_prepends_user_message_when_containers_unequal_length(self):
        expect(lambda:
                   expect([0]).withUserMessage("userMessage").toEqual([])).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")
        
    def test_tuple_comparse_to_equivalent_list(self):
        expect((1, 2)).toEqual([1, 2])

class ContainerNotExpectationsTests(TestCase):
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

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
        expect(lambda: expect([0, 1]).withUserMessage("userMessage").Not.toBeASupersetOf([0])).toRaise(
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
