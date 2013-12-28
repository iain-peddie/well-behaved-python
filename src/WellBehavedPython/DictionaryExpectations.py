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
import WellBehavedPython.api;

class DictionaryExpectations(DefaultExpectations):
    
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
    
    def toEqual(self, expected):        
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is equal 
        to the expected value.

        Inputs
        ------
        expected : the value that the actual value is expected to equal

        Exceptions
        ----------
        AssertionError : raised if self.actual does not equal expected.
"""
        if len(self.actual) == len(expected):
            message = self.buildMessage("to equal ", expected)
            failCount = 0
            for key in self.actual.keys():
                failCount += self._checkKey(key, expected, message)
            if failCount == 0:
                self.success(message)
        else:
            message = self.buildMessage("to be a dictionary containing ", len(expected), extra = " items")
            self.fail(message)

    def toContainKey(self, expected):
        """Asserts that self.actual has expected as a key. 

        Inputs
        ------
        expected: The key that is expected to be contained within self.actual

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""

        message = self.buildMessage('to contain key ', expected)
        if expected in self.actual:
            self.success(message)
        else:
            self.fail(message)

    def toContainValue(self, expected):
        """Asserts that self.actual has expected as a value against any key. 

        Inputs
        ------
        expected: The value that is expected to be contained within self.actual

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""
        message = self.buildMessage('to contain value ', expected)
        if expected in self.actual.values():
            self.success(message)
        else:
            self.fail(message)

    def _checkKey(self, key, expected, message):
        formattedKey = self.formatForMessage(key)
        if key not in expected:
            message += "\nFirst missing key is {}".format(formattedKey)
            self.fail(message)
            return 1
        else:
            message += "\nFirst difference at key {}".format(formattedKey)
            try:
                # We use try/catch and a local fail clause so that
                # if this is a expect.Not... then we have the correct
                # strategy logic
                WellBehavedPython.api.expect(self.actual[key]).withUserMessage(message).toEqual(expected[key])
            except AssertionError as ex:
                self.fail(ex.args[0])
                return 1

        return 0
                
