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

from .DefaultExpectations import DefaultExpectations
from .Expect import *
from .ExpectNot import *

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

    def expect(self, actual):
        """Creates an appropriate expectations object for using on actual.

        This searches through the list of registered factories until one
        which matches actual is found, and then uses that to create the
        actual object."""
        factory = self._factories[0]
        strategy = Expect()
        reverseStrategy = ExpectNot()
        
        return factory.createExpectations(actual, strategy, reverseStrategy) 

    def register(self, creationPredicate, createExpectations):
        self._factories[0] = ExpectationsFactory(creationPredicate, 
                                                 createExpectations)

    def _createDefaultExpecationsFactory(self):
        return ExpectationsFactory(
            lambda actual: True, 
            DefaultExpectations)

