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

from .Expect import *
from .ExpectNot import *
from .MethodSpy import *

from .ContainerExpectations import *
from .DictionaryExpectations import *
from .NumericExpectations import *
from .StringExpectations import *
from .MethodSpyExpectations import *
from .ExpectationsRegistry import *

from .typeInference import *

def expect(actual, normal = True):
    """Facade for creating expectation objects.

    This will eventually create a specialised expectation object
    based on the class type."""

    if normal:
        strategy = Expect()
        reverseStrategy = ExpectNot()
    else:
        strategy = ExpectNot()
        reverseStrategy = Expect()

    expectationsFactories = []
    expectationsFactories.append(ExpectationsFactory(
            lambda actual: isinstance(actual, str), 
            StringExpectations))
    expectationsFactories.append(ExpectationsFactory(
            lambda actual: isDictionary(actual), 
            DictionaryExpectations))
    expectationsFactories.append(ExpectationsFactory(
            lambda actual: isIterable(actual),
            ContainerExpectations))
    expectationsFactories.append(ExpectationsFactory(
            lambda actual: isNumeric(actual), 
            NumericExpectations))
    expectationsFactories.append(ExpectationsFactory(
            lambda actual: isinstance(actual, MethodSpy),
            MethodSpyExpectations))
    expectationsFactories.append(ExpectationsFactory(
            lambda actual: True, 
            DefaultExpectations))

    for factory in expectationsFactories:
        if factory.shouldUseFor(actual):
            return factory.createExpectations(actual, strategy, reverseStrategy)
        
def spyOn(method):
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
    method : a object method object. Can be specified as object.method. """

    instance = method.__self__
    name = method.__name__
    spy = MethodSpy(methodName = name, methodObject = method)
    instance.__dict__[name] = spy
    return spy

