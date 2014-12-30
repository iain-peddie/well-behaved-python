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

from .ArrayExpectations import ArrayExpectations

from numpy import *

class ThreeVectorExpectations(ArrayExpectations):
    
    def toBeCollinearWith(self, expected, tolerance = 1e-5):
        """Tests whether expected is collinear with actual.

        Note that for this definition collinear means parallel within
        tolerance or antiparallel within tolernace.

        Note that the test is ||(a X e) / (||a|| ||e||)|| > tolerance, where
        a is actual, e is expected, X represents the cross product and ||x|| is
        the 2-norm of x

        Inputs
        ------
        expected: The expected value for actual to be tested for
                  collinearity with.
        tolerance: The tolerance for closeness."""

        self._compareTypes(expected)
        
        message = self._compareSizes(expected)
        if message:
            self.fail(message)
            return

        na = linalg.norm(self.actual)
        ne = linalg.norm(expected)

        message = self.buildMessage("to be collinear with ", expected)

    
        if na < 1e-16 or ne < 1e-16:
            self.fail(message)
            return

        metric = linalg.norm(cross(self.actual, expected))/(na * ne)
        if metric > tolerance:
            self.fail(message)
        else:
            self.success(message)

    def toBePerpendicularTo(self, expected, tolerance = 1e-5):
        """Tests whether expected is collinear with actual.

        Note that for this definition collinear means parallel within
        tolerance or antiparallel within tolernace.

        Note that the test is (a . e) / (||a|| ||e||) > tolerance, where
        a is actual, e is expected, X represents the cross product and ||x|| is
        the 2-norm of x

        Inputs
        ------
        expected: The expected value for actual to be tested for
                  collinearity with.
        tolerance: The tolerance for closeness."""

        self._compareTypes(expected)
        
        message = self._compareSizes(expected)
        if message:
            self.fail(message)
            return

        na = linalg.norm(self.actual)
        ne = linalg.norm(expected)

        message = self.buildMessage("to be perpendicular to ", expected)
        metric = dot(self.actual, expected)/ (na*ne)

        if metric > tolerance:
            self.fail(message)
        else:
            self.success(message)
