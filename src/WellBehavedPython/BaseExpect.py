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

import re;

class BaseExpect:
    """Base class for handling expectation logic, which is our
    equivalent of asserting in standard TDD frameworks.

    The class is intended to be used by chaining the constructor
    to the expected condition, for example:

    a = 2
    Expect(a).toEqual(2)."""
    
    def __init__(self, actual):
        """Constructor

        Inputs
        ------
        actual : the actual value to be considered."""
        self.actual = actual

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

    def _compareTypes(self, expected):
        """Asserts that the types of self and expected are equal.

        Inputs
        ------
        expected:  the expected value, whose type will be compared to
                   the type of self.actual

        Exceptions
        ----------
        AssertionError : raised if the types of self and self.value are incompatible.
"""

        # NOTE
        # we compare by exact type matching, not isinstance because
        # we don't want to do comparisons for equality, greater than if the
        # types are fundamentally different. Expect("abc").toEqual(6) makes
        # no sense, for example.

        # Users may want to compare for the same type; that is an assertion
        # and should be a separate public method.
        
        # We want to compare types first. We also want this to
        # bypass the usual overriding of type comparison semantics.
        # Otherwise Expect(5).Not.toBeGreaterThan("6") will pass, when
        # it should really fail not (5 > "6") would throw an exception
        # and we should keep the same sematics here. 

        actualType = type(self.actual)
        expectedType = type(expected)

        message = "Cannot compare instance of {} to instance of {} because their types differ".format(
            actualType, expectedType)

        # NOTE we don't use pass and fail, because we want do have direct
        # control over the failure semantics. ExpectNot(1).toEqual("1") should
        # still fail - a comparison of objects of different types should always
        # fail as that indicates a more fundamental problem with the test

        assert actualType == expectedType, message

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

    def toContain(self, expectedContainee, userMessage = ""):
        """Indicates a success case if self.actual contains expectedContainee,
        and a failure otherwise        

        Inputs
        ------
        expectedContainee      : The item that self.actual is expected to contain
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""
        message = self.buildMessage("to contain ", expectedContainee, userMessage)
        if expectedContainee in self.actual:
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

    def toRaise(self, exceptionClass, userMessage = "", expectedMessage = None):
        from .Expect import Expect
        try:
            self.actual()
        except BaseException as ex:
            message = self.buildRaiseMessage(exceptionClass, ex, expectedMessage, userMessage)

            if isinstance(ex, exceptionClass):

                if expectedMessage != None and expectedMessage != ex.args[0]:
                    message = message
                    self.fail(message)
                else:
                    self.success(message)
                return
            self.fail(message)

        message = self.buildMessage("to raise an instance of ", exceptionClass,
                                        userMessage, ", but none was")
        self.fail(message)


    def buildRaiseMessage(self, exceptionClass, ex, expectedMessage, userMessage):
        extra = ", but it raised an instance of {}".format(type(ex))
        
        if expectedMessage == None:
            operation = "to raise an instance of "
            comparison = exceptionClass
        else:
            operation = "to raise an instance of {} with message ".format(exceptionClass)
            comparison = expectedMessage
            extra = extra + " with message {}".format(self.formatForMessage(ex.args[0]))

        message = self.buildMessage(operation, comparison, 
                                        userMessage, extra)
        return message
        

    def formatForMessage(self, unformatted):
        """Perform formatting for special types which need to be formatted
        differently, e.g. strings to indicate where their start and ends are.

        Inputs
        ------
        unformatted : the unformatted value

        Returns
        -------
        The correctly formatted output, if the standard python formatting will
        not be acceptable.
"""
        if isinstance(unformatted, str):
            return "'{}'".format(unformatted)
        formatted = "{}".format(unformatted)
        match = re.match("(<.*) at[^>]*(>)", formatted)
        if match:
            formatted =  "".join(match.groups([1,2]))
        return formatted

    def _buildMessage(self, operation, expected, userMessage, extra):
        """Builds the message that goes into assertion messages

        Inputs
        ------
        operation : a string containing the comparison operation,
            .e.g 'to equal'
        expected : the expected value in the comparison (if there
            is one)
        userMessage: message from the user to be prepended onto the
            whole message.
        extra: appended to the message

        Returns
        -------
        The full, built message to go into AssertionError if one
        is raised.
"""
           
        formattedActual = self.formatForMessage(self.actual);
        if expected:
            formattedExpected = self.formatForMessage(expected)
        else:
            formattedExpected = ""

        if userMessage and len(userMessage) > 0:
            prepend = userMessage + ": "
        else:
            prepend = ""

        return "{}Expected {} {}{}{}".format(prepend, 
                                            formattedActual, 
                                            operation,
                                            formattedExpected,
                                            extra)


