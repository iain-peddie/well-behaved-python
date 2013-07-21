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
        message = self.buildMessage("to be greater than ", expected, userMessage);
        if self.actual > expected:
            self.success(message)
        else:
            self.fail(message)

    def toBeGreaterThanOrEqualTo(self, expected, userMessage = ""):
        message = self.buildMessage("to be greater than or equal to ", expected, userMessage);
        if self.actual >= expected:
            self.success(message)
        else:
            self.fail(message)

    def toBeLessThan(self, expected, userMessage = ""):
        message = self.buildMessage("to be less than ", expected, userMessage)
        if self.actual < expected:
            self.success(message)
        else:
            self.fail(message)
