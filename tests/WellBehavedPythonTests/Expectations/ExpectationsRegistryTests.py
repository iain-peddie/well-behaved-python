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
from WellBehavedPython.Expectations.DefaultExpectations import DefaultExpectations
from WellBehavedPython.Expectations.ExpectationsRegistry import *

class ExpectationsFactoryTests(TestCase):

    def test_that_factory_says_should_not_create_when_predicate_is_False(self):
        # Where
        factory = ExpectationsFactory(lambda klass: False, None)

        # When
        result = factory.shouldUseFor(1)

        # Then
        expect(result).toBeFalse()
        
    def test_that_factory_says_should_create_when_predicate_is_True(self):
        # Where
        factory = ExpectationsFactory(lambda klass: True, None)

        # When
        result = factory.shouldUseFor(1)

        # Then
        expect(result).toBeTrue()

    def test_that_factory_creates_expect_and_expect_not_methods(self):
        # Where
        self.createCallCount = 0
        self.reverser = None

        def create_expecter(actual, strategy, reverser):
            self.createCallCount += 1
            if reverser is not None:
                self.reverser = reverser
            return 'mockExpecter'

        factory = ExpectationsFactory(lambda item: True, create_expecter)
        item = 1

        # When

        factory.createExpectations(item, 'mockStrategy', 'mockReverseStrategy')

        # Then
        expect(self.createCallCount).toEqual(2)
        expect(self.reverser).toEqual('mockExpecter')

class ExpectationsRegistryTests(TestCase):
    
    def test_that_creation_using_a_fresh_registry_creates_default_expectations(self):
        # Where
        actual = {'a': 'b'}
        registry = self.createDefaultExpectationsRegistry()

        # When
        expectations = registry.expect(actual)

        # Then
        expect(expectations).toBeAnInstanceOf(DefaultExpectations)

    def test_that_default_expectations_object_can_be_used(self):
        # Where
        registry = self.createDefaultExpectationsRegistry()
        expect1 = registry.expect(1)
        
        # When
        expect1.toEqual(1)
        expect1.Not.toEqual(2)

    def test_that_registered_expectations_beat_default(self):
        # Where
        registry = self.createDefaultExpectationsRegistry()

        # When
        registry.register(isNumeric, NumericExpectations)
        expect1 = registry.expect(1)

        # Then
        expect(expect1).toBeAnInstanceOf(NumericExpectations)

    def test_that_registry_uses_creation_predicates(self):
        # Where
        registry = self.createRegistryWithNumericsRegistered()
        expect(isNumeric('asdf')).toBeFalse()

        # When
        expectAsdf = registry.expect('asdf')

        # Then
        # NumericExpectations are derived from DefaultExpectations, 
        # so we can't test is an instance of Default (class derivation
        # is an isa relationship, so a NumericExpectations is a DefaultExpcetations,
        # so instead we check that expectAsdf is not a NumericExpectations)
        
        expect(expectAsdf).Not.toBeAnInstanceOf(NumericExpectations)

    def createDefaultExpectationsRegistry(self):
        return ExpectationsRegistry();

    def createRegistryWithNumericsRegistered(self):
        registry = self.createDefaultExpectationsRegistry()
        registry.register(isNumeric, NumericExpectations)
        return registry

class ExpectationsRegistryNumpyTests(TestCase):
    """These tests should only be run if numpy is installed."""

    def before(self):
        self.defaultRegistry = ExpectationsRegistry.createDefaultExpectationsRegistry()
    
    def test_registration_gives_ContainerExpectations_for_3_2_ndarray_by_default(self):
        # Where
        registry = self.defaultRegistry
        numpyArray = self.createNumpyArray(3, 2)
        
        # When
        expecter = registry.expect(numpyArray)

        # Then
        expect(expecter).toBeAnInstanceOf(ContainerExpectations)

    def test_registration_gives_ArrayExpectations_for_3_2_ndarray_after_registering_numpy_expectations(self):
        from WellBehavedPython.Expectations.Numpy.ArrayExpectations import ArrayExpectations
        from WellBehavedPython.Expectations.Numpy.SquareMatrixExpectations import SquareMatrixExpectations

        # Where
        registry = self.defaultRegistry
        numpyArray = self.createNumpyArray(3, 2)
        
        # When
        registry.registerNumpyExpectations()
        expecter = registry.expect(numpyArray)

        # Then
        expect(expecter).toBeAnInstanceOf(ArrayExpectations)        
        expect(expecter).Not.toBeAnInstanceOf(SquareMatrixExpectations)

    def test_registration_gives_ArrayExpectations_for_2_ndarray_after_registering_numpy_expectations(self):
        from WellBehavedPython.Expectations.Numpy.ArrayExpectations import ArrayExpectations
        from WellBehavedPython.Expectations.Numpy.ThreeVectorExpectations import ThreeVectorExpectations

        # Where
        registry = self.defaultRegistry
        numpyArray = self.createNumpyArray(2)
        
        # When
        registry.registerNumpyExpectations()
        expecter = registry.expect(numpyArray)

        # Then
        expect(expecter).toBeAnInstanceOf(ArrayExpectations)
        expect(expecter).Not.toBeAnInstanceOf(ThreeVectorExpectations)

    def test_registration_gives_ThreeVectorExpectations_for_3_ndarray_after_registering_numpy_expectations(self):
        from WellBehavedPython.Expectations.Numpy.ThreeVectorExpectations import ThreeVectorExpectations

        # Where
        registry = self.defaultRegistry
        numpyArray = self.createNumpyArray(3)
        
        # When
        registry.registerNumpyExpectations()
        expecter = registry.expect(numpyArray)

        # Then
        expect(expecter).toBeAnInstanceOf(ThreeVectorExpectations)        

    def test_registration_of_square_matrix_uses_SquareMatrixExpectations(self):
        from WellBehavedPython.Expectations.Numpy.SquareMatrixExpectations import SquareMatrixExpectations

        # Where
        registry = self.defaultRegistry
        numpyArray = self.createNumpyArray(3,3)
        
        # When
        registry.registerNumpyExpectations()
        expecter = registry.expect(numpyArray)

        # Then
        expect(expecter).toBeAnInstanceOf(SquareMatrixExpectations)        

    def test_registration_via_api(self):
        from WellBehavedPython.Expectations.Numpy.SquareMatrixExpectations import SquareMatrixExpectations
        from WellBehavedPython.Expectations.Numpy.ThreeVectorExpectations import ThreeVectorExpectations
        from WellBehavedPython.Expectations.Numpy.ArrayExpectations import ArrayExpectations


        # Where
        vector = self.createNumpyArray(3)
        nonsquareMatrix = self.createNumpyArray(2, 3)
        squareMatrix = self.createNumpyArray(3, 3)
        
        # When
        registerNumpy()
        vectorExpectations = expect(vector)
        nonsquareExpectations = expect(nonsquareMatrix)
        squareExpectations = expect(squareMatrix)

        # Then
        expect(vectorExpectations).toBeAnInstanceOf(ThreeVectorExpectations)
        expect(nonsquareExpectations).toBeAnInstanceOf(ArrayExpectations)
        expect(squareExpectations).toBeAnInstanceOf(SquareMatrixExpectations)
        

    def createNumpyArray(self, width, height = None):
        from numpy import zeros

        if height is not None:
            return zeros([width, height])
        else:
            return zeros(width)
        

