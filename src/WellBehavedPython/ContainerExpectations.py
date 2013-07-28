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

    def toBeASupersetOf(self, expected, userMessage = ""):
        """Indicates a success case if every item in expected is in self.actual

        Inputs
        ------
        expected      : The container of items that should all be in self.actual
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""
        expectedSet = self._setFromObject(expected)
        actualSet = self._setFromObject(self.actual);

        message = self.buildMessage("to be a superset of ", expected, userMessage)

        if actualSet.issuperset(expectedSet):
            self.success(message)
        else:
            self.fail(message)

    def toBeASubsetOf(self, expected):
        """Indicates a success case if every item in self.actual is in expected

        Inputs
        ------
        expected      : The container of items some of which should be in self.actual
        userMessage (optional) : a message that is prepended to the assertion
                                 error message if the condition fails. This
                                 allows users to get a quicker identification
                                 of the line in a test which is failing if more
                                 than one value is being tested for equality.

        Exceptions
        ----------
        AssertionError : may be raised by success or fail
"""
        expectedSet = self._setFromObject(expected)
        actualSet = self._setFromObject(self.actual);

        message = self.buildMessage("to be a subset of ", expected, "")

        if actualSet.issubset(expectedSet):
            self.success(message)
        else:
            self.fail(message)

    def _setFromObject(self, obj):
        if not isinstance(obj, Iterable):
            obj = [obj];
        return frozenset(obj);











