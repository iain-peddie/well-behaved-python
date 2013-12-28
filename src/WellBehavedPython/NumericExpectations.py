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

    def toBeGreaterThan(self, expected):
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is greater than
        the expected value.

        Inputs
        ------
        expected : the value that the actual value is expected to be greater than

        Exceptions
        ----------
        AssertionError : may be raised by sucess or fail.
"""
        message = self.buildMessage("to be greater than ", expected, self.userMessage);
        if self.actual > expected:
            self.success(message)
        else:
            self.fail(message)

    def toBeGreaterThanOrEqualTo(self, expected):
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is greater than
        or equal to the expected value.

        Inputs
        ------
        expected : The value that the actual value is expected to be greater than
                   or equal to.

        Exceptions
        ----------
        AssertionError : may be raised by sucess or fail.
"""
        message = self.buildMessage("to be greater than or equal to ", expected, self.userMessage);
        if self.actual >= expected:
            self.success(message)
        else:
            self.fail(message)

    def toBeLessThan(self, expected):
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is less than
        the expected value.

        Inputs
        ------
        expected : the value that the actual value is expected to be less than

        Exceptions
        ----------
        AssertionError : may be raised by sucess or fail.
"""
        message = self.buildMessage("to be less than ", expected, self.userMessage)
        if self.actual < expected:
            self.success(message)
        else:
            self.fail(message)

    def toBeLessThanOrEqualTo(self, expected):
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is less than
        the expected value.

        Inputs
        ------
        expected : the value that the actual value is expected to be less than
                   or equal to.

        Exceptions
        ----------
        AssertionError : may be raised by sucess or fail.
"""
        message = self.buildMessage("to be less than or equal to ", expected, self.userMessage)
        if self.actual <= expected:
            self.success(message)
        else:
            self.fail(message)
        
    def toEqual(self, expected, userMessage = "", tolerance = 1e-8, toleranceType = ""):
        self._compareTypes(expected)

        FLOOR_TOLERANCE = 1e-20

        try:
            abs(expected)
            abs(self.actual)
        except:
            DefaultExpectations.toEqual(self, expected, userMessage)
            return

        if toleranceType == "absolute":
            difference = abs(self.actual - expected)
        else:
            # floor tolerance means we don't accidentally divide by zero
            difference = abs(self.actual -  expected)*2 / (abs(self.actual) + abs(expected) + FLOOR_TOLERANCE)
            toleranceType = "relative"


        if isinstance(self.actual, int) and isinstance(expected, int):
            toleranceMessage = ""
        else:
            toleranceMessage = " within {} tolerance of {}".format(toleranceType, tolerance)       

        message = self.buildMessage("to equal ", expected, userMessage,
                                    toleranceMessage)
        if difference < tolerance:
            self.success(message)
        else:        
            self.fail(message)

