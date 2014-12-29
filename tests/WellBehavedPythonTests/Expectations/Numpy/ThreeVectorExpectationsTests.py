#!/usr/bin/env python3

# Copyright 2013-4 Iain Peddie inr314159@hotmail.com
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

from WellBehavedPython.api import *
from WellBehavedPython.Engine.TestCase import *
from WellBehavedPython.Expectations.Numpy.ThreeVectorExpectations import *

from numpy import *

class ThreeVectorExpectationsTestCase(TestCase):

    def before(self):
        self.expecter = ExpectationsRegistry.createDefaultExpectationsRegistry()
        self.expecter.register(lambda x: isinstance(x, ndarray), ThreeVectorExpectations)

    def _createVector(self, a, b, c):
        return array([a, b, c])

class ToBeCollinearWithTests(ThreeVectorExpectationsTestCase):
    
    def test_same_vectors_considered_collinear(self):
        # Where
        v1 = self._createVector(1, 0, 0)
        v2 = v1.copy()

        # When
        shouldPass = lambda: self.expecter.expect(v1).toBeCollinearWith(v2)
        shouldFail = lambda: self.expecter.expect(v1).Not.toBeCollinearWith(v2)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[.*\] not to be collinear with \[.*\]")

    def test_misaligned_vectors_not_considered_collinear(self):
        # Where
        v1 = self._createVector(1, 0, 0)
        v2 = self._createVector(1, 0, 1e-4)

        # When
        shouldFail = lambda: self.expecter.expect(v1).toBeCollinearWith(v2)
        shouldPass = lambda: self.expecter.expect(v1).Not.toBeCollinearWith(v2)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[.*\] to be collinear with \[.*\]")
