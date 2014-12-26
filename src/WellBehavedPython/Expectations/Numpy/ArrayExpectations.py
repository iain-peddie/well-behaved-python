#!/usr/bin/env python3

# Copyright 2014 Iain Peddie inr314159@hotmail.com
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

from ..DefaultExpectations import *

from numpy import *

class ArrayExpectations(DefaultExpectations):

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
        self._compareTypes(expected)
        failMessage = self._compareSizes(expected)
        if failMessage is not None:
            self.fail(failMessage)
            return # don't carry forward if we're in a not contenxt            


        comparison = equal(self.actual, expected)
        extraMessageParts = ["\nFor equality with tolerance, use toEqualWithinRelativeTolerance" 
        + " or toEqualWithinAbsoluteTolerance"]
        extraMessageParts.append(self._createDifferenceLocationMessage(comparison))

        message = self.buildMessage("to exactly equal ", expected, 
                                    extra = "\n".join(extraMessageParts))


        if all(comparison):
            self.success(message)
        else:
            self.fail(message)

    def _compareSizes(self, expected):
        if self.actual.ndim != expected.ndim:
            return "Dimensionality mismatch when comparing ndarrays: {} != {}".format(
                self.actual.ndim, expected.ndim)
            

        if self.actual.shape != expected.shape:
            if self.actual.ndim > 1:
                return "Shape mismatch: {} != {}".format(self.actual.shape, expected.shape)
            else:
                return "Size mismatch: {} != {}".format(self.actual.size, expected.size)

        return None

    def _createDifferenceLocationMessage(self, comparisonResults):
        flippedResults = ~comparisonResults
        if comparisonResults.ndim == 1:
            locations = flatnonzero(flippedResults)            
            if len(locations) == 0:
                return "no differences"
            firstLocation = locations[0]
            return "First difference is at [{}]".format(firstLocation)

        else:
            locations = transpose(flippedResults.nonzero())
            if len(locations) == 0:
                return "no differences"
            firstLocation = locations[0]
            return "First difference is at {}".format(firstLocation)


        
