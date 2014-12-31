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
from WellBehavedPython.Expectations.Numpy.SquareMatrixExpectations import *

from numpy import *

class SquareMatrixExpectationsTestCase(TestCase):

    def before(self):
        self.expecter = ExpectationsRegistry.createDefaultExpectationsRegistry()
        self.expecter.register(lambda x: isinstance(x, ndarray), SquareMatrixExpectations)

class ToBeInvertibleTests(SquareMatrixExpectationsTestCase):

    def test_identity_considered_invertible(self):
        # Where
        
        i3 = identity(3)
        
        # When
        shouldPass = lambda: self.expecter.expect(i3).toBeInvertible()
        shouldFail = lambda: self.expecter.expect(i3).Not.toBeInvertible()

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] not to be invertible")

    def test_diag_120_not_considered_invertible(self):
        # Where
        m = diag([1, 2, 0])        
        
        # When
        shouldFail = lambda: self.expecter.expect(m).toBeInvertible()
        shouldPass = lambda: self.expecter.expect(m).Not.toBeInvertible()

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] to be invertible")

class ToBeOrthogonalTests(SquareMatrixExpectationsTestCase):

    def test_identity_considered_orthogonal(self):
        # Where
        
        i3 = identity(3)
        
        # When
        shouldPass = lambda: self.expecter.expect(i3).toBeOrthogonal()
        shouldFail = lambda: self.expecter.expect(i3).Not.toBeOrthogonal()

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] not to be orthogonal")

    def test_projection_matrix_not_considered_orthogonal(self):
        # Where        
        p = array([[0, 1], 
                   [0, 0]])
        
        # When
        shouldFail = lambda: self.expecter.expect(p).toBeOrthogonal()
        shouldPass = lambda: self.expecter.expect(p).Not.toBeOrthogonal()

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] to be orthogonal")

    def test_not_quite_orthogonal_matrix_not_considered_orthogonal(self):
        # Where        
        p = array([[0, 1], 
                   [1+1.1e-10, 0]])
        
        # When
        shouldFail = lambda: self.expecter.expect(p).toBeOrthogonal(absoluteTolerance=1e-10)
        shouldPass = lambda: self.expecter.expect(p).Not.toBeOrthogonal(absoluteTolerance=1e-10)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] to be orthogonal")
        

    def test_just_orthogonal_matrix_not_considered_orthogonal(self):
        # Where        
        p = array([[0, 1], 
                   [1+0.99e-10, 0]])
        
        # When
        shouldPass = lambda: self.expecter.expect(p).toBeOrthogonal(absoluteTolerance=1e-10)
        shouldFail = lambda: self.expecter.expect(p).Not.toBeOrthogonal(absoluteTolerance=1e-10)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] not to be orthogonal")
        
class ToBeHermitianTests(SquareMatrixExpectationsTestCase):

    def test_identity_considered_hermitian(self):
        # Where
        
        i3 = identity(3)
        
        # When
        shouldPass = lambda: self.expecter.expect(i3).toBeHermitian()
        shouldFail = lambda: self.expecter.expect(i3).Not.toBeHermitian()

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] not to be hermitian")

    def test_pauli_matrix_sigma2_considered_hermitian(self):
        # Where
        sigma2 = array([[ 0, -1j],
                        [1j, 0]])

        # When
        shouldPass = lambda: self.expecter.expect(sigma2).toBeHermitian()
        shouldFail = lambda: self.expecter.expect(sigma2).Not.toBeHermitian()

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] not to be hermitian")


    def test_projection_matrix_not_considered_orthogonal(self):
        # Where        
        p = array([[0, 1j], 
                   [0, 0]])
        
        # When
        shouldFail = lambda: self.expecter.expect(p).toBeHermitian()
        shouldPass = lambda: self.expecter.expect(p).Not.toBeHermitian()

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] to be hermitian")

    def test_not_quite_orthogonal_matrix_not_considered_orthogonal(self):
        # Where        
        p = array([[0, 1], 
                   [1+1.1e-10j, 0]])
        
        # When
        shouldFail = lambda: self.expecter.expect(p).toBeHermitian(absoluteTolerance=1e-10)
        shouldPass = lambda: self.expecter.expect(p).Not.toBeHermitian(absoluteTolerance=1e-10)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] to be hermitian")
        

    def test_just_orthogonal_matrix_not_considered_orthogonal(self):
        # Where        
        p = array([[0, 1], 
                   [1+0.99e-10j, 0]])
        
        # When
        shouldPass = lambda: self.expecter.expect(p).toBeHermitian(absoluteTolerance=1e-10)
        shouldFail = lambda: self.expecter.expect(p).Not.toBeHermitian(absoluteTolerance=1e-10)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "\] not to be hermitian")

