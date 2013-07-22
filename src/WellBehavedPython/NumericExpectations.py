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

from .DefaultExpectations import *;

class NumericExpectations(DefaultExpectations):

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

        DefaultExpectations.__init__(self, actual, strategy, reverseExpecter)

    def toBeGreaterThan(self, expected, userMessage = ""):
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is greater than
        the expected value.

        Inputs
        ------
        expected : the value that the actual value is expected to be greater than
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by sucess or fail.
"""
        message = self.buildMessage("to be greater than ", expected, userMessage);
        if self.actual > expected:
            self.success(message)
        else:
            self.fail(message)

    def toBeGreaterThanOrEqualTo(self, expected, userMessage = ""):
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is greater than
        or equal to the expected value.

        Inputs
        ------
        expected : The value that the actual value is expected to be greater than
                   or equal to.
        userMessage (optional) : A message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by sucess or fail.
"""
        message = self.buildMessage("to be greater than or equal to ", expected, userMessage);
        if self.actual >= expected:
            self.success(message)
        else:
            self.fail(message)

    def toBeLessThan(self, expected, userMessage = ""):
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is less than
        the expected value.

        Inputs
        ------
        expected : the value that the actual value is expected to be less than
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by sucess or fail.
"""
        message = self.buildMessage("to be less than ", expected, userMessage)
        if self.actual < expected:
            self.success(message)
        else:
            self.fail(message)

    def toBeLessThanOrEqualTo(self, expected, userMessage = ""):
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is less than
        the expected value.

        Inputs
        ------
        expected : the value that the actual value is expected to be less than
                   or equal to.
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by sucess or fail.
"""
        message = self.buildMessage("to be less than or equal to ", expected, userMessage)
        if self.actual <= expected:
            self.success(message)
        else:
            self.fail(message)
        