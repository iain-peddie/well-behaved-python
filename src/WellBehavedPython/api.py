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

from .Discovery.TestDiscoverer import *
from .Engine.TestContext import *
from .Expectations.ExpectationsRegistry import *
from .Fakes.MethodSpy import *


_registry = ExpectationsRegistry.createDefaultExpectationsRegistry()

def expect(actual):
    """Facade for creating expectation objects.

    This will eventually create a specialised expectation object
    based on the class type."""

    return _registry.expect(actual)

def withUserMessage(message):
    """Facade for creating test contexts."""

    return TestContext(_registry, message)


def discoverTests(name, ignoreFilters=[]):
    discoverer = TestDiscoverer()
    return discoverer.buildSuiteFromModuleName(name, ignoreFilters = ignoreFilters)

def registerExpectationClass(usePredicate, constructor):
    """Way of registereing new expectation classes.

    Registration acts in a last registration wins scenario.

    Inputs
    ------
    usePredicate: expected to be callable taking one argument.
    
                  Inputs
                  ------
                  actual: The value being considered for expectations
                          
                  Returns
                  -------
                  True, if the actual value is appropriate for use in
                  with the registered Expectations object
                  False otherwise

                  Examples
                  -------
                  isNumeric
                  lambda actual: isinstance(actual, timedelta)

    constructor: Expected to construct an expectations object. 

                 Inputs
                 ------
                 actual: the actual value to be expected against
                 strategy: the strategy to use for passing and failing
                           This should usually be either an instance of
                           Expect or an instance of ExpectNot
                 reverseExpecter: The reverse object. This should either
                                  be another instance of what this constructor
                                  returns, or None

                 Returns
                 -------
                 A created expectation object

                 Example
                 -------
                 NumericExpectations
                 lambda actual, strategy, reverser: 
                           NumericExpecations(float(actual), strategy, reverser)."""
    _registry.register(usePredicate, constructor)
        
def spyOn(methodOrObject):
    """spies on a given method.

    Takes the given object method, creates a test spy and replaces the 
    method in it's own instance with the test spy. This allows objects
    to be changed dynamically and allows test to have the form

    spyOn(object.method)
    # ...
    expect(object.method).toHaveBeenCalled()
    
    Which is a highly expressive way of writing tests.

    Inputs
    ------
    methodOrObject : a object method object. Can be specified as object.method. """

    import types

    argType = type(methodOrObject)
    
    if argType == types.MethodType:
        return spyOnMethod(methodOrObject)
    else:
        
        methods = [method for method in dir(methodOrObject) if callable(getattr(methodOrObject, method))]
        for methodName in methods:
            if methodName.startswith('_'):
                continue
            method = getattr(methodOrObject, methodName)
            spyOnMethod(method)
        return methodOrObject

def spyOnMethod(method):

    instance = method.__self__
    name = method.__name__
    spy = MethodSpy(methodName = name, methodObject = method)
    instance.__dict__[name] = spy
    return spy

