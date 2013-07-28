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

import re

from .BaseExpect import BaseExpect



class DefaultExpectations(BaseExpect):
    
    def __init__(self, actual, strategy, reverseExpecter = None):
        """Constructor

        Inputs
        ------
        actual : the actual value to be compared against.
        strategy: the strategy to take on pass or fail methods
        reverseExpecter (optional) : an expecter that has the opposite semantics.
                  BaseExpect will store this in the Not field, allowing expect(a).Not...
                  to behave in the obvious way.
        """

        BaseExpect.__init__(self, actual, strategy, reverseExpecter)

    def toEqual(self, expected, userMessage = None):
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is equal 
        to the expected value.

        Inputs
        ------
        expected : the value that the actual value is expected to equal
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : raised if self.actual does not equal expected.
"""
        self._compareTypes(expected)
        message = self.buildMessage("to equal ", expected, userMessage);
        if self.actual == expected:
            self.success(message)
        else:        
            self.fail(message)

    def toBeTrue(self, userMessage = ""):
        """Asserts that self.expected is something that evaluates true,
        that is True, a non-zero number or a non-empty collection.

        Inputs
        ------
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""

        message = self.buildMessage("to be True", None, userMessage)
        if self.actual:
            self.success(message)
        else:
            self.fail(message)

    def toBeFalse(self, userMessage = ""):
        """Asserts that self.expected is something that evaulautes false,
        that is False, a zero number or an empty collection.

        Inputs
        ------
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""

        message = self.buildMessage("to be False", None, userMessage)
        if self.actual:
            self.fail(message)
        else:
            self.success(message)

    def toBeNone(self, userMessage = ""):
        """Indicates a success case if self.actual is None, and a failure otherwise        

        Inputs
        ------
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""

        message = self.buildMessage("to be None", None, userMessage)
        if self.actual is not None:
            self.fail(message)
        else:
            self.success(message)

    def toBeIn(self, expectedContainer, userMessage = ""):
        """Indicates a success case if self.actual is in expectedContainer, 
        and a failure otherwise        

        Inputs
        ------
        expectedContainer :      The container that is expected to contain
                                 self.actual
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""
        message = self.buildMessage("to be in ", expectedContainer, userMessage)
        if self.actual in expectedContainer:
            self.success(message)
        else:
            self.fail(message)


    def toBeAnInstanceOf(self, klass, userMessage = ""):
        """Indicates a success case if self.actual is an instance of klass,
        and a failure otherwise        

        Inputs
        ------
        klass     : The expected class/type of the actual item
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""
        message = self.buildMessage("to be an instance of ", klass, userMessage,
                                     " but was an instance of {}".format(
                type(self.actual)))
        if isinstance(self.actual, klass):
            self.success(message)
        else:
            self.fail(message)

    def toRaise(self, exceptionClass, userMessage = "", expectedMessage = None, expectedMessageMatches = None):
        from .Expect import Expect
        ex = None

        try:
            self.actual()
        except BaseException as _ex:
            ex = _ex

        if ex is not None:
            message = self.buildRaiseMessage(exceptionClass, ex, expectedMessage, expectedMessageMatches, userMessage)
            if isinstance(ex, exceptionClass):

                if expectedMessage != None and expectedMessage != ex.args[0]:
                    self.fail(message)
                elif expectedMessageMatches != None and not re.search(expectedMessageMatches, ex.args[0]):                    
                    self.fail(message)
                else:
                    self.success(message)
            else:
                self.fail(message)
            
        else:    
            message = self.buildMessage("to raise an instance of ", exceptionClass,
                                        userMessage, ", but none was")
            self.fail(message)


    def buildRaiseMessage(self, exceptionClass, ex, expectedMessage, expectedMessageMatches, userMessage):
        """Builds the message that goes into expected exception assertion messages

        Inputs
        ------
        exceptionClass: the expected class of the exception
        ex: the actual exception object that was caught
        expectedMessage: the complete expected exception message
        expectedMessageMatches: a string or compiled regular expression
              which the exception message is expected to match
        userMessage: message from the user to be prepended onto the
            whole message.

        Returns
        -------
        The full, built message to go into AssertionError if one
        is raised."""


        extra = ", but it raised an instance of {}".format(type(ex))
        
        if expectedMessage == None and expectedMessageMatches == None:
            operation = "to raise an instance of "
            comparison = exceptionClass
        
        else: 
            operation = "to raise an instance of {} with message ".format(exceptionClass)
            comparison = expectedMessage
            if expectedMessageMatches != None:
                operation = operation + "matching regular expression "
                if type(expectedMessageMatches) == str:
                    comparison = expectedMessageMatches
                elif str(type(expectedMessageMatches)) == "<class '_sre.SRE_Pattern'>":
                    comparison = expectedMessageMatches.pattern
                else:
                    raise AssertionError("Expected message patterns must be strings or "
                                         "compiled regex patterns. Object type is {}".format(
                            type(expectedMessageMatches)))

                

            extra = extra + " with message {}".format(self.formatForMessage(ex.args[0]))            

        message = self.buildMessage(operation, comparison, 
                                        userMessage, extra)
        return message
