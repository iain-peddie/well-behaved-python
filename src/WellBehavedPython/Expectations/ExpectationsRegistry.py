#!/usr/bin/env python3

# Copyright 2013-5 Iain Peddie inr314159@hotmail.com
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

from ..Engine.Expect import *
from ..Engine.ExpectNot import *


from .DefaultExpectations import DefaultExpectations
from .ContainerExpectations import *
from .DictionaryExpectations import *
from .NumericExpectations import *
from .StringExpectations import *
from .MethodSpyExpectations import *

from .typeInference import *


class ExpectationsFactory:
    """Class responsible for creating and configureing an Expectations object.

    The ExpectationsRegistry will use a collection of these to decide which
    expectations object to create for each item."""

    def __init__(self, createPredicate, createExpectations):
        """Constructor

        Inputs
        ------
        createPredicate: callable item which returns True or False
                         depending on whether it's argument is appropriate
                         for the type of ExpectationsObject this factory
                         is configured to create
        createExpectations: callable object that is used to create
                            an expectations object in isolation."""

        self._createPredicate = createPredicate
        self._createExpectations = createExpectations

    def shouldUseFor(self, item):
        return self._createPredicate(item)

    def createExpectations(self, item, strategy, reverseStrategy):
        reverseExpectations = self._createExpectations(item, reverseStrategy, None)
        expectations = self._createExpectations(item, strategy, reverseExpectations)

        return expectations

class ExpectationsRegistry:
    """Class that holds a priority ordered set of expectations factories and matching rules.

    Later rules are found first, thus allowing for a full customisation of the rule set.
    In principle, adding a rule which always matches, then any futher rules will be equivalent
    to entirely replacing the set of registered expectations factories (as the search will
    never go past the match all rule."""

    def __init__(self):
        """Default constructor."""
        self._factories = [ self._createDefaultExpecationsFactory() ]

    @staticmethod
    def createDefaultExpectationsRegistry():
        registry = ExpectationsRegistry()
        registry.register(lambda actual: isinstance(actual, MethodSpy),
                           MethodSpyExpectations)
        registry.register(lambda actual: isinstance(actual, timedelta), 
                           NumericExpectations)
        registry.register(lambda actual: isinstance(actual, datetime), 
                           NumericExpectations)
        registry.register(isNumeric,
                           NumericExpectations)        
        registry.register(isIterable, ContainerExpectations)
        registry.register(isDictionary, DictionaryExpectations)
        registry.register(lambda actual: isinstance(actual, str), 
                          StringExpectations)
        return registry


    def expect(self, actual):
        """Creates an appropriate expectations object for using on actual.

        This searches through the list of registered factories until one
        which matches actual is found, and then uses that to create the
        actual object."""
        strategy = Expect()
        reverseStrategy = ExpectNot()

        for factory in reversed(self._factories):
            if not factory.shouldUseFor(actual):
                continue
            return factory.createExpectations(actual, strategy, reverseStrategy) 


    def register(self, creationPredicate, createExpectations):
        """Registers a new expectations class with a given creation predicate.

        This can be used to set custom rules appropriate for your custom classes,
        or for common external modules that are integral to what you are doing.
        For instance, if you're doing a lot of image analysis using OpenCV, you
        might want to write your own class to assert on the OpenCV data types 
        coming our of your algorithms...

        Note that registration acts as a stack, so your expectations will be tried
        first. As such, if you have more than one rule to add, register the more
        generic thing first, then the more specialised thing.

        Inputs
        ------
        creationPredicate: A callable object that takes an object, and returns
               whether or not createExpectations shoudl be created for it.
               e.g. lambda item: isinstance(item, str)
        createExpectations: A callable object that has the same signature as
               DefaultExpectations and returns the correctly consturcted
               expectations object. Can usually be a constructor. If your
               expectations object has more inputs, you will need to register
               it with a lambda that gives specific values to the extra parameters."""
        
        self._factories.append(ExpectationsFactory(creationPredicate, 
                                                   createExpectations))

    def registerNumpyExpectations(self):
        """Registers the Numpy specific expectations against this registratio
        object. This should only be called if numpy is installed on your system.
        Otherwise you will likely get errors. (And if not, will be uncecessarily
        slowing down the tests)."""

        from numpy import ndarray
        from WellBehavedPython.Expectations.Numpy.ArrayExpectations import ArrayExpectations

        self.register(lambda item: isinstance(item, ndarray), ArrayExpectations)
        
    

    def _createDefaultExpecationsFactory(self):
        return ExpectationsFactory(
            lambda actual: True, 
            DefaultExpectations)

