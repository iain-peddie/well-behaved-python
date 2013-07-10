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

    def test_fail_doesnt_raise_anything(self):
        ExpectNot(True).fail()
        # pass condition should be that we get to this point

    def test_success_raises_AssertionError(self):
        raised = True
        try:
            ExpectNot(True).success("Message")
            raised = False
        except AssertionError as ex:
            Expect(ex.args[0]).toEqual("Message")
        Expect(raised).toBeTrue("Expected an AssertionError to be raised")

    def test_equals_doesnt_raise_if_numbers_unequal(self):
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
        
        Expect(raised).toBeTrue("Expected an AssertionError to be raised")
        Expect(message).toEqual("Expected 1 not to equal 1")

    def test_equals_doesnt_raise_if_two_strings_unequal(self):
        ExpectNot("asdf").toEqual("zxc")

    def test_equals_raises_correctly_if_strings_equal(self):
        raised = False
        message = ""
        try:
            ExpectNot("asdf").toEqual("asdf")
        except AssertionError as ex:
            raised = True
            message = ex.args[0]
        
        Expect(raised).toBeTrue("Expected an AssertionError to be raised")
        Expect(message).toEqual("Expected 'asdf' not to equal 'asdf'")        

    def test_expecting_string1_not_to_equal_double1_fails(self):
        raised = False
        try:
            Expect("1").toEqual(1)
        except AssertionError as ex:
            raised = True
            Expect(ex.args[0]).toEqual("Cannot compare instance of <class 'str'> to "
                                       + "instance of <class 'int'> because their types differ")
        
        Expect(raised).toBeTrue("Expected an AssertionError to be raised")

    def test_expect_truthy_values_not_to_be_true_fails(self):
        values = (True, 1, (1))
        actualMessages = []
        expectedMessages = ("Expected True not to be True",
                          "Expected 1 not to be True", 
                          "Expected (1) not to be True")
        for value in values:
            try:
                ExpectNot(value).toBeTrue()
            except AssertionError as ex:
                actualMessages.append(ex.args[0])

        Expect(len(actualMessages)).toEqual(len(expectedMessages))
        for i in range(0, len(expectedMessages) - 1):
            Expect(actualMessages[i]).toEqual(expectedMessages[i])

    def test_expect_falsy_values_not_to_be_true_succeeds(self):
        values = (False, 0, ())
        for value in values:
            ExpectNot(value).toBeTrue()

    def test_expect_truthy_values_not_to_be_false_succeeds(self):
        values = (True, 1, (1))
        for value in values:
            ExpectNot(value).toBeFalse()

    def test_expect_falsy_values_not_to_be_false_fails(self):
        values = (False, 0, ())
        actualMessages = []
        expectedMessages = ("Expected False not to be False",
                          "Expected 0 not to be False", 
                          "Expected () not to be False")
        for value in values:
            try:
                ExpectNot(value).toBeFalse()
            except AssertionError as ex:
                actualMessages.append(ex.args[0])

        Expect(len(actualMessages)).toEqual(len(expectedMessages))
        for i in range(0, len(expectedMessages) - 1):
            Expect(actualMessages[i]).toEqual(expectedMessages[i])

    def test_expect_not_true_prepends_usermessage_to_assertion(self):
        try:
            ExpectNot(True).toBeTrue("user message")
        except AssertionError as ex:
            Expect(ex.args[0]).toEqual("user message: Expected True not to be True")

    def test_expect_not_false_prepends_usermessage_to_assertion(self):
        try:
            ExpectNot(False).toBeFalse("user message")
        except AssertionError as ex:
            Expect(ex.args[0]).toEqual("user message: Expected False not to be False")

    def test_expect_not_False_toBeNone_passes(self):
        ExpectNot(False).toBeNone()

    def test_expect_not_None_toBeNone_fails_with_correct_message(self):
        message = ""
        try:
            ExpectNot(None).toBeNone()
        except AssertionError as ex:
            message = ex.args[0]
        
        Expect(message).toEqual("Expected None not to be None")

    def test_expect_not_toBeNone_prepends_userMessage(self):
        message = ""
        try:
            ExpectNot(None).toBeNone("user message")
        except AssertionError as ex:
            message = ex.args[0]
        Expect(message).toEqual("user message: Expected None not to be None")

    def test_expect_not_x_to_be_in_y_passes_when_x_is_not_in_y(self):
        x = 602
        y = [601, 603, 605]
        ExpectNot(x).toBeIn(y)

    def test_expect_not_x_to_be_in_y_raises_AssertionError_when_x_in_y(self):
        x = 602
        y = [601, x, 603]
        message = ""
        try:
            ExpectNot(x).toBeIn(y)
        except AssertionError as ex:
            message = ex.args[0]
        
        Expect(message).toEqual("Expected 602 not to be in [601, 602, 603]")

    def test_expect_not_x_to_be_in_y_raises_AssertionError_when_item_equal_to_x_in_y(self):
        x = 602
        y = [601, 602, 603]
        message = ""
        try:
            ExpectNot(x).toBeIn(y)
        except AssertionError as ex:
            message = ex.args[0]
        
        Expect(message).toEqual("Expected 602 not to be in [601, 602, 603]")
    
    def test_expect_not_x_to_be_in_y_prepends_usermessage_on_failure(self):
        x = 602
        y = [601, 602, 603]
        message = ""
        try:
            ExpectNot(x).toBeIn(y, "user message")
        except AssertionError as ex:
            message = ex.args[0]
        
        Expect(message).toEqual("user message: Expected 602 not to be in [601, 602, 603]")

    def test_expect_not_y_to_contain_x_passes_when_x_not_in_y(self):
        x = 602
        y = [601, 603, 605]
        ExpectNot(y).toContain(x)

    def test_expect_not_y_to_contain_x_fails_when_x_in_y(self):
        x = 602
        y = [601, 602, 603]
        message = ""
        try:
            ExpectNot(y).toContain(x)
        except AssertionError as ex:
            message = ex.args[0]
        
        Expect(message).toEqual("Expected [601, 602, 603] not to contain 602")
        
    def test_expect_not_y_to_contain_x_prepends_usermessage(self):
        x = 602
        y = [601, 602, 603]
        message = ""
        try:
            ExpectNot(y).toContain(x, "user message")
        except AssertionError as ex:
            message = ex.args[0]
        
        Expect(message).toEqual("user message: Expected [601, 602, 603] not to contain 602")
        
    def test_expect_not_1_instanceof_float_passes(self):
        ExpectNot(1).toBeAnInstanceOf(float)

    def test_expect_not_1_instanceof_int_fails(self):
        message = ""
        try:
            ExpectNot(1).toBeAnInstanceOf(int)
        except AssertionError as ex:
            message = ex.args[0]
        Expect(message).toEqual("Expected 1 not to be an instance of <class 'int'> but was an instance of <class 'int'>")

    def test_expect_not_self_instanceof_TestResults_passes(self):
        ExpectNot(self).toBeAnInstanceOf(TestResults)

    def test_expect_not_self_instanceof_ExpectNotTests_fails(self):
        message = ""
        try:
            ExpectNot(self).toBeAnInstanceOf(ExpectNotTests)
        except AssertionError as ex:
            message = ex.args[0]
        Expect(message).toEqual("Expected <ExpectNotTests.ExpectNotTests object> not to be an instance of <class 'ExpectNotTests.ExpectNotTests'> but was an instance of <class 'ExpectNotTests.ExpectNotTests'>")

    def expect_not_self_instanceof_TestCase_fails(self):
        message = ""
        try:
            ExpectNot(self).toBeAnInstanceOf(TestCase)
        except AssertionError as ex:
            message = ex.args[0]
        Expect(message).toEqual("Expected <ExpectNotTests.ExpectNotTests object> not to be an instance of <class 'WellBehavedPython.TestCase.TestCase'> but was an instance of <class 'ExpectNotTests.ExpectNotTests'>")        

    def test_instance_of_prepends_usermessage(self):
        message = ""
        try:
            ExpectNot(1).toBeAnInstanceOf(int, "user message")
        except AssertionError as ex:
            message = ex.args[0]
        Expect(message).toEqual("user message: Expected 1 not to be an instance of <class 'int'> but was an instance of <class 'int'>")
        

if __name__ == "__main__":
    suite = ExpectNotTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())
