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

# list of exceptions for comparing types. Each key is a type, and the value
# is a tuple of types which are considered 'equivalent' for the purposes
# of comparing values
typeComparisonExceptions = {
    int: (int, float),
    float: (float, int) ,
    tuple: (tuple, list),
    list: (list, tuple),
    set: (set, frozenset),
    frozenset: (frozenset, set)
}

class BaseExpect:
    """Base class for handling expectation logic, which is our
    equivalent of asserting in standard TDD frameworks.

    The class is intended to be used by chaining the constructor
    to the expected condition, for example:

    a = 2
    Expect(a).toEqual(2)."""
    
    def __init__(self, actual, strategy, reverseExpecter):
        """Constructor

        Inputs
        ------
        actual : the actual value to be considered."""
        self.actual = actual
        self.strategy = strategy
        self.Not = reverseExpecter

    def fail(self, message = ""):
        """Indicate a test condition has failed.

        Responsibility is transferred to the strategy object.

        Inputs
        ------
        message(optional) : Message to be passed to the raised AssertionError.
        """

        self.strategy.fail(message)

    def success(self, message = ""):
        """Indicate a test condition has succeeded.

        Inputs
        ------
        message(optional) : ignored. Part of the BaseExpect interface.
        """
        self.strategy.success(message)

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


        if type(unformatted) == "_sre.SRE_Pattern":
            unformatted = unformatted.pattern

        if isinstance(unformatted, str):
            return "'{}'".format(unformatted)
        formatted = "{}".format(unformatted)
        match = re.match("(<.*) at[^>]*(>)", formatted)
        if match:
            formatted =  "".join(match.groups([1,2]))
        return formatted

    def buildMessage(self, operation, expected, userMessage, extra = ""):
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

        operation = self.strategy.decorateOperation(operation)
           
        formattedActual = self.formatForMessage(self.actual)
        if expected is not None:
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



        if actualType in typeComparisonExceptions.keys():
            if expectedType in typeComparisonExceptions[actualType]:
                return

        assert actualType == expectedType, message
        
