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
from WellBehavedPython.ExpectNot import *
from WellBehavedPython.Expect import *

class ExpectNotTests(TestCase):
    
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    @staticmethod
    def suite():
        testMethods = [
            "test_fail_doesnt_raise_anything",
            "test_success_raises_AssertionError",
            "test_equals_success_if_numbers_unequal",
            "test_equals_raises_correctly_if_numbers_equal",
#            "test_equals_doesnt_raise_if_string_items_are_equal",
#            "test_equals_raises_with_right_message_if_string_items_not_equal"
            ]
        
        suite = TestSuite()
    
        for testMethod in testMethods:
            suite.add(ExpectNotTests(testMethod))
        return suite

    def test_fail_doesnt_raise_anything(self):
        ExpectNot(True).fail()
        # pass condition should be that we get to this point

    def test_success_raises_AssertionError(self):
        flag = True
        try:
            ExpectNot(True).success("Message")
            flag = False
        except AssertionError as ex:
            Expect(ex.args[0]).toEqual("Message")
        assert flag, "Expected AssertionError to have been thrown, but nothing was"

    def test_equals_success_if_numbers_unequal(self):
        ExpectNot(1).toEqual(2)
        # Pass condition if we get here with no exception

    def test_equals_raises_correctly_if_numbers_equal(self):
        raised = False
        message = ""
        try:
            ExpectNot(1).toEqual(1)
        except AssertionError as ex:
            raised = True
            message = ex.args[0]
        
        assert raised, "Expected exception to be thrown"
        Expect(message).toEqual("Expected 1 not to equal 1")

        


if __name__ == "__main__":
    suite = ExpectNotTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())
