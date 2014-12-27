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
        self._compareElements(expected, absoluteTolerance = 0, relativeTolerance = 0, messageStub = "to exactly equal ")

    def toBeCloseTo(self, expected, absoluteTolerance = None, relativeTolerance = None):
        self._compareElements(expected, absoluteTolerance, relativeTolerance, "to be close to ")
        

    def _compareElements(self, expected, absoluteTolerance, relativeTolerance, messageStub):
        self._compareTypes(expected)
        failMessage = self._compareSizes(expected)
        if failMessage is not None:
            self.fail(failMessage)
            return # don't carry forward if we're in a not contenxt            

        if absoluteTolerance is None:
            if relativeTolerance is None:
                comparison = isclose(self.actual, expected)
            else:
                comparison = isclose(self.actual, expected, atol=0, rtol = relativeTolerance)
        else:
            if relativeTolerance is None:
                comparison = isclose(self.actual, expected, atol=absoluteTolerance, rtol = 0)
            else:                        
                comparison = isclose(self.actual, expected, atol = absoluteTolerance, 
                             rtol=relativeTolerance)

        extraMessageParts = []
        extraMessageParts.append(self._createDifferenceCountMessage(comparison))
        extraMessageParts.append(self._createDifferenceLocationMessage(comparison))

        extraMessage = "\n" + "\n".join(extraMessageParts)
        message = self.buildMessage(messageStub, expected, 
                                    extra = extraMessage)

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

    def _createDifferenceCountMessage(self, comparisonResults):
        numDifferences = count_nonzero(~comparisonResults)
        numElements = comparisonResults.size
        if numDifferences < numElements:
            return "{} out of {} elements differ".format(
            numDifferences, numElements)
        else:
            return "all elements differ"

    def _createDifferenceLocationMessage(self, comparisonResults):
        flippedResults = ~comparisonResults
        locations = transpose(flippedResults.nonzero())
        if len(locations) == 0:
            return "no differences"
        firstLocation = locations[0]
        return "First difference is at {}".format(firstLocation)


        
