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
from WellBehavedPython.Expectations.Numpy.ArrayExpectations import *

from numpy import *

class ArrayExpectationsTests(TestCase):

    def before(self):
        self.expecter = ExpectationsRegistry.createDefaultExpectationsRegistry()
        self.expecter.register(lambda x: isinstance(x, ndarray), ArrayExpectations)
        
    def _createVector(self, numCols):
        return zeros(numCols)

    def _createMatrix(self, numRows, numCols):
        return zeros([numRows, numCols])

    def _createTensor(self, numRows, numCols, numLayers):
        return zeros([numRows, numCols, numLayers])


class ToEqualTests(ArrayExpectationsTests):
    
    def test_identical_vectors_considered_equal(self):
        # Where
        v1 = self._createVector(3)
        v2 = v1.copy()

        # Then
        expect(lambda: self.expecter.expect(v1).Not.toEqual(v2)).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[\s*0\.\s+0\.\s+0\.\] not to exactly equal \[\s*0\.\s+0\.\s+0\.\]")

    def test_vectors_differing_at_1e_minus_16_considered_unequal(self):
        # Where
        v1 = self._createVector(3)
        v2 = v1.copy()
        v2[2] = 1e-16

        # Then
        expect(lambda: self.expecter.expect(v1).toEqual(v2)).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[\s*0\.\s+0\.\s+0\.\] to exactly equal \[\s*0\.0+e\+0+\s+0\.0+e\+0+\s+1\.0+e-16\]")

    def test_identical_matrices_considered_equal(self):
        # Where
        m1 = self._createMatrix(3,2)
        m2 = m1.copy()

        # Then
        expect(lambda: self.expecter.expect(m1).Not.toEqual(m2)).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected (\[(?:\[\s*0\.\s+0\.\s*\]\s*){3}\]) not to exactly equal \\1")

    def test_matrices_differing_at_1e_minus_16_considered_unequal(self):
        # Where
        m1 = self._createMatrix(3, 2)
        m2 = m1.copy()
        m2[2,1] = 1e-16

        # Then
        expect(lambda: self.expecter.expect(m1).toEqual(m2)).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected (\[(?:\[\s*0\.\s+0\.\s*\]\s*){3}\]) to exactly equal \[(\[\s*0\.0+e\+00\s+.0\.0+e\+00*\]\s*){2}\[\s*0\.0+e\+00\s+.1\.0+e-16*\]\]")

    def test_vector_equal_to_matrix_fails(self):
        # Where
        m = self._createMatrix(3, 2)
        v = self._createVector(3)

        # Then
        expect(lambda: self.expecter.expect(v).toEqual(m)).toRaise(
            AssertionError,
            expectedMessage = "Dimensionality mismatch when comparing ndarrays: 1 != 2")
        expect(lambda: self.expecter.expect(m).toEqual(v)).toRaise(
            AssertionError,
            expectedMessage = "Dimensionality mismatch when comparing ndarrays: 2 != 1")

    def test_vector_not_equal_to_matrix_passes(self):
        # Where
        m = self._createMatrix(3, 2)
        v = self._createVector(3)

        # When
        self.expecter.expect(v).Not.toEqual(m)
        self.expecter.expect(m).Not.toEqual(v)

        # Then
        # (no assertions were raised)

    def test_vectors_of_different_sizes_equals_fails(self):
        # Where
        v1 = self._createVector(2)
        v2 = self._createVector(3)

        # Then
        expect(lambda: self.expecter.expect(v1).toEqual(v2)).toRaise(
            AssertionError,
            expectedMessage = "Size mismatch: 2 != 3")
        expect(lambda: self.expecter.expect(v2).toEqual(v1)).toRaise(
            AssertionError,
            expectedMessage = "Size mismatch: 3 != 2")

    def test_vectors_of_different_sizes_not_equals_passes(self):
        # Where
        v1 = self._createVector(2)
        v2 = self._createVector(3)

        # When
        self.expecter.expect(v1).Not.toEqual(v2)
        self.expecter.expect(v2).Not.toEqual(v1)

        # Then
        # (no assertions were raised)

    def test_matrices_of_different_num_rows_equals_fails(self):
        # Where
        m1 = self._createMatrix(2, 3)
        m2 = self._createMatrix(3, 3)

        # Then
        expect(lambda: self.expecter.expect(m1).toEqual(m2)).toRaise(
            AssertionError,
            expectedMessage = "Shape mismatch: (2, 3) != (3, 3)")
        expect(lambda: self.expecter.expect(m2).toEqual(m1)).toRaise(
            AssertionError,
            expectedMessage = "Shape mismatch: (3, 3) != (2, 3)")

    def test_matrices_of_different_num_rows_not_equals_passes(self):
        # Where
        m1 = self._createMatrix(2, 3)
        m2 = self._createMatrix(3, 3)

        # When
        self.expecter.expect(m1).Not.toEqual(m2)
        self.expecter.expect(m2).Not.toEqual(m1)

        # Then
        # (no expections are raised)

    def test_matrices_of_different_num_cols_equals_fails(self):
        # Where
        m1 = self._createMatrix(3, 2)
        m2 = self._createMatrix(3, 3)

        # Then
        expect(lambda: self.expecter.expect(m1).toEqual(m2)).toRaise(
            AssertionError,
            expectedMessage = "Shape mismatch: (3, 2) != (3, 3)")
        expect(lambda: self.expecter.expect(m2).toEqual(m1)).toRaise(
            AssertionError,
            expectedMessage = "Shape mismatch: (3, 3) != (3, 2)")

    def test_matrices_of_different_num_cols_not_equals_passes(self):
        # Where
        m1 = self._createMatrix(3, 2)
        m2 = self._createMatrix(3, 3)

        # When
        self.expecter.expect(m1).Not.toEqual(m2)
        self.expecter.expect(m2).Not.toEqual(m1)

        # Then
        # (no expections are raised)

    def test_index_of_difference_in_vector_given(self):
        # Where
        v1 = self._createVector(3)
        v2 = v1.copy()
        v2[2] = 1e-16

        # When
        expect(lambda: self.expecter.expect(v1).toEqual(v2)).toRaise(
            AssertionError,
            expectedMessageMatches = "First difference is at \[2\]")

    def test_index_of_difference_in_matrix_given(self):
        # Where
        m1 = self._createMatrix(3, 3)
        m2 = m1.copy()
        m2[0,2] = 1e-16
        m2[1,1] = 1

        # When
        expect(lambda: self.expecter.expect(m1).toEqual(m2)).toRaise(
            AssertionError,
            expectedMessageMatches = "First difference is at \[0 2\]")

    def test_index_of_difference_in_tensor_given(self):
        # Where
        t1 = self._createTensor(3, 3, 3)
        t2 = t1.copy()
        t2[0,1,2] = 1e-16
        t2[1,1,1] = 1

        # When
        expect(lambda: self.expecter.expect(t1).toEqual(t2)).toRaise(
            AssertionError,
            expectedMessageMatches = "First difference is at \[0 1 2\]")

    def test_that_toEqual_indicates_number_of_differences_for_vectors(self):
        # Where
        v1 = self._createVector(3)
        v2 = v1.copy()
        v2[1] = 1e-16
        v2[2] = 2e-16

        # Then
        expect(lambda: self.expecter.expect(v1).toEqual(v2)).toRaise(
            AssertionError,
            expectedMessageMatches = "2 out of 3 elements differ")

    def test_that_toEqual_indicates_number_of_differences_for_matrices(self):
        # Where
        m1 = self._createMatrix(3, 3)
        m2 = m1.copy()
        m2[0,2] = 1e-16
        m2[1,1] = 1
        m2[-1,-1] = 1e-5

        # Then
        expect(lambda: self.expecter.expect(m1).toEqual(m2)).toRaise(
            AssertionError,
            expectedMessageMatches = "3 out of 9 elements differ")

    def test_that_toEqual_indicates_when_all_elements_differ(self):
        # Where
        v1 = zeros(3)
        v2 = ones(3)

        # When
        expect(lambda: self.expecter.expect(v1).toEqual(v2)).toRaise(
            AssertionError,
            expectedMessageMatches = "all elements differ")
        
        
class ToBeCloseToTests(ArrayExpectationsTests):

    def test_that_identical_vectors_considered_close(self):
        # Where
        v1 = self._createVector(3)
        v2 = v1.copy()

        # When
        shouldFail = lambda: self.expecter.expect(v1).Not.toBeCloseTo(v2)

        # Then
        self.expecter.expect(v1).toBeCloseTo(v2)
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected (\[\s*0\.\s+0\.\s+0\.\]) not to be close to \\1")

    def test_that_identical_matrices_considered_close(self):
        # Where
        m1 = self._createMatrix(3,2)
        m2 = m1.copy()

        # Then
        expect(lambda: self.expecter.expect(m1).Not.toBeCloseTo(m2)).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected (\[(?:\[\s*0\.\s+0\.\s*\]\s*){3}\]) not to be close to \\1")

    def test_that_elements_just_inside_absolute_tolerance_considered_close(self):
        # Where
        tolerance = 1e-8
        tiny = 1e-16
        v1 = self._createVector(3)
        
        v2 = v1 + (tolerance - tiny)
        
        # When
        shouldFail = lambda: self.expecter.expect(v1).Not.toBeCloseTo(v2, absoluteTolerance=tolerance)
        shouldPass = lambda: self.expecter.expect(v1).toBeCloseTo(v2, absoluteTolerance=tolerance)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[.*\] not to be close to \[.*\]")

    def test_that_elements_just_inside_outside_absolute_tolerance_considered_not_close(self):
        # Where
        tolerance = 1e-8
        tiny = 1e-16
        v1 = self._createVector(3)
        
        v2 = v1 + (tolerance + tiny)
        
        # When
        shouldPass = lambda: self.expecter.expect(v1).Not.toBeCloseTo(v2, absoluteTolerance=tolerance)
        shouldFail = lambda: self.expecter.expect(v1).toBeCloseTo(v2, absoluteTolerance=tolerance)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[.*\] to be close to \[.*\]")

    def test_that_elements_just_inside_relative_tolerance_considered_close(self):
        # Where
        tolerance = 1e-5
        delta = tolerance
        v1 = ones(3)
        
        v2 = v1.copy()
        v2[2] = 1+delta
        
        # When
        shouldFail = lambda: self.expecter.expect(v1).Not.toBeCloseTo(v2, relativeTolerance=tolerance)
        shouldPass = lambda: self.expecter.expect(v1).toBeCloseTo(v2, relativeTolerance=tolerance)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[.*\] not to be close to \[.*\]")

    def test_that_elements_just_inside_outside_relative_tolerance_considered_not_close(self):
        # Where
        tolerance = 1e-5
        delta = 2*tolerance
        v1 = ones(3)
        
        v2 = v1.copy()
        v2[2] = 1+delta
        
        # When
        shouldPass = lambda: self.expecter.expect(v1).Not.toBeCloseTo(v2, relativeTolerance=tolerance)
        shouldFail = lambda: self.expecter.expect(v1).toBeCloseTo(v2, relativeTolerance=tolerance)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[.*\] to be close to \[.*\]")

    def test_that_default_tolerances_forgiving(self):
        # Where
        v1 = ones(3)
        
        v2 = v1.copy()
        v2[2] = 1+1e-10

        # When
        shouldFail = lambda: self.expecter.expect(v1).Not.toBeCloseTo(v2)
        shouldPass = lambda: self.expecter.expect(v1).toBeCloseTo(v2)

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[.*\] not to be close to \[.*\]")
        
    def test_vector_close_to_matrix_fails(self):
        # Where
        m = self._createMatrix(3, 2)
        v = self._createVector(3)

        # Then
        expect(lambda: self.expecter.expect(v).toBeCloseTo(m)).toRaise(
            AssertionError,
            expectedMessage = "Dimensionality mismatch when comparing ndarrays: 1 != 2")
        expect(lambda: self.expecter.expect(m).toBeCloseTo(v)).toRaise(
            AssertionError,
            expectedMessage = "Dimensionality mismatch when comparing ndarrays: 2 != 1")

    def test_vector_not_close_to_matrix_passes(self):
        # Where
        m = self._createMatrix(3, 2)
        v = self._createVector(3)

        # When
        self.expecter.expect(v).Not.toBeCloseTo(m)
        self.expecter.expect(m).Not.toBeCloseTo(v)

        # Then
        # (no assertions were raised)

    def test_vectors_of_different_sizes_equals_fails(self):
        # Where
        v1 = self._createVector(2)
        v2 = self._createVector(3)

        # Then
        expect(lambda: self.expecter.expect(v1).toBeCloseTo(v2)).toRaise(
            AssertionError,
            expectedMessage = "Size mismatch: 2 != 3")
        expect(lambda: self.expecter.expect(v2).toBeCloseTo(v1)).toRaise(
            AssertionError,
            expectedMessage = "Size mismatch: 3 != 2")

    def test_vectors_of_different_sizes_not_equals_passes(self):
        # Where
        v1 = self._createVector(2)
        v2 = self._createVector(3)

        # When
        self.expecter.expect(v1).Not.toBeCloseTo(v2)
        self.expecter.expect(v2).Not.toBeCloseTo(v1)

        # Then
        # (no assertions were raised)

    def test_matrices_of_different_num_rows_equals_fails(self):
        # Where
        m1 = self._createMatrix(2, 3)
        m2 = self._createMatrix(3, 3)

        # Then
        expect(lambda: self.expecter.expect(m1).toBeCloseTo(m2)).toRaise(
            AssertionError,
            expectedMessage = "Shape mismatch: (2, 3) != (3, 3)")
        expect(lambda: self.expecter.expect(m2).toBeCloseTo(m1)).toRaise(
            AssertionError,
            expectedMessage = "Shape mismatch: (3, 3) != (2, 3)")

    def test_matrices_of_different_num_rows_not_equals_passes(self):
        # Where
        m1 = self._createMatrix(2, 3)
        m2 = self._createMatrix(3, 3)

        # When
        self.expecter.expect(m1).Not.toBeCloseTo(m2)
        self.expecter.expect(m2).Not.toBeCloseTo(m1)

        # Then
        # (no expections are raised)

    def test_matrices_of_different_num_cols_equals_fails(self):
        # Where
        m1 = self._createMatrix(3, 2)
        m2 = self._createMatrix(3, 3)

        # Then
        expect(lambda: self.expecter.expect(m1).toBeCloseTo(m2)).toRaise(
            AssertionError,
            expectedMessage = "Shape mismatch: (3, 2) != (3, 3)")
        expect(lambda: self.expecter.expect(m2).toBeCloseTo(m1)).toRaise(
            AssertionError,
            expectedMessage = "Shape mismatch: (3, 3) != (3, 2)")

    def test_matrices_of_different_num_cols_not_equals_passes(self):
        # Where
        m1 = self._createMatrix(3, 2)
        m2 = self._createMatrix(3, 3)

        # When
        self.expecter.expect(m1).Not.toBeCloseTo(m2)
        self.expecter.expect(m2).Not.toBeCloseTo(m1)

        # Then
        # (no expections are raised)


######
    def test_index_of_difference_in_vector_given(self):
        # Where
        v1 = self._createVector(3)
        v2 = v1.copy()
        v2[2] = 1e-4

        # When
        expect(lambda: self.expecter.expect(v1).toBeCloseTo(v2)).toRaise(
            AssertionError,
            expectedMessageMatches = "First difference is at \[2\]")

    def test_index_of_difference_in_matrix_given(self):
        # Where
        m1 = self._createMatrix(3, 3)
        m2 = m1.copy()
        m2[0,2] = 1e-4
        m2[1,1] = 1

        # When
        expect(lambda: self.expecter.expect(m1).toBeCloseTo(m2)).toRaise(
            AssertionError,
            expectedMessageMatches = "First difference is at \[0 2\]")

    def test_index_of_difference_in_tensor_given(self):
        # Where
        t1 = self._createTensor(3, 3, 3)
        t2 = t1.copy()
        t2[0,1,2] = 1e-4
        t2[1,1,1] = 1

        # When
        expect(lambda: self.expecter.expect(t1).toBeCloseTo(t2)).toRaise(
            AssertionError,
            expectedMessageMatches = "First difference is at \[0 1 2\]")

    def test_that_toEqual_indicates_number_of_differences_for_vectors(self):
        # Where
        v1 = self._createVector(3)
        v2 = v1.copy()
        v2[1] = 1e-4
        v2[2] = 2e-4

        # Then
        expect(lambda: self.expecter.expect(v1).toBeCloseTo(v2)).toRaise(
            AssertionError,
            expectedMessageMatches = "2 out of 3 elements differ")

    def test_that_toEqual_indicates_number_of_differences_for_matrices(self):
        # Where
        m1 = self._createMatrix(3, 3)
        m2 = m1.copy()
        m2[0,2] = 1e-4
        m2[1,1] = 1
        m2[-1,-1] = 1e-3

        # Then
        expect(lambda: self.expecter.expect(m1).toBeCloseTo(m2)).toRaise(
            AssertionError,
            expectedMessageMatches = "3 out of 9 elements differ")

    def test_that_toEqual_indicates_when_all_elements_differ(self):
        # Where
        v1 = zeros(3)
        v2 = ones(3)

        # When
        expect(lambda: self.expecter.expect(v1).toBeCloseTo(v2)).toRaise(
            AssertionError,
            expectedMessageMatches = "all elements differ")


class ToBeRealTests(ArrayExpectationsTests):
    
    def test_that_real_matrix_considered_real(self):
        # Where
        m1 = zeros([3,3], complex)

        # When
        shouldPass = lambda: self.expecter.expect(m1).toBeReal()
        shouldFail = lambda: self.expecter.expect(m1).Not.toBeReal()

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[(\[.*\]\s*){3}\] not to be real")

    def test_that_almost_real_matrix_not_considered_real(self):
        # Where
        m1 = zeros([3,3], complex)
        m1[0:3,0:3] = 1+1j
        
        # When
        shouldPass = lambda: self.expecter.expect(m1).Not.toBeReal()
        shouldFail = lambda: self.expecter.expect(m1).toBeReal()

        # Then
        shouldPass()
        expect(shouldFail).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected \[(\[.*\]\s*){3}\] to be real")
