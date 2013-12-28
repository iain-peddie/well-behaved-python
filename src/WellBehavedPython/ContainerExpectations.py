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

from collections import Iterable

class ContainerExpectations(DefaultExpectations):

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
        self._compareTypes(expected)
        if len(self.actual) == len(expected):
            message = self.buildMessage("to equal ", expected, self.userMessage)
            for i in range(0, len(self.actual)):
                if self.actual[i] != expected[i]:
                    message = message + "\nFirst difference at index {}: {} != {}".format(
                        i, self.actual[i], expected[i])
                    self.fail(message)
                    return        


            self.success(message)
        else:        
            message = self.buildMessage("to be a container of length ", len(expected), self.userMessage);
            self.fail(message)


    def toContain(self, expectedContainee):
        """Indicates a success case if self.actual contains expectedContainee,
        and a failure otherwise        

        Inputs
        ------
        expectedContainee      : The item that self.actual is expected to contain

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""
        message = self.buildMessage("to contain ", expectedContainee, self.userMessage)
        if expectedContainee in self.actual:
            self.success(message)
        else:
            self.fail(message)

    def toBeASupersetOf(self, expected):
        """Indicates a success case if every item in expected is in self.actual

        Inputs
        ------
        expected      : The container of items that should all be in self.actual

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""
        expectedSet = self._setFromObject(expected)
        actualSet = self._setFromObject(self.actual);

        message = self.buildMessage("to be a superset of ", expected, self.userMessage)

        if actualSet.issuperset(expectedSet):
            self.success(message)
        else:
            self.fail(message)

    def toBeASubsetOf(self, expected):
        """Indicates a success case if every item in self.actual is in expected

        Inputs
        ------
        expected      : The container of items some of which should be in self.actual

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""
        expectedSet = self._setFromObject(expected)
        actualSet = self._setFromObject(self.actual);

        message = self.buildMessage("to be a subset of ", expected, self.userMessage)

        if actualSet.issubset(expectedSet):
            self.success(message)
        else:
            self.fail(message)

    def _setFromObject(self, obj):
        if not isinstance(obj, Iterable):
            obj = [obj];
        return frozenset(obj);











