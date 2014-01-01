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

from .ExpectationsRegistry import *
from .MethodSpy import *

_registry = ExpectationsRegistry.createDefaultExpectationsRegistry()

def expect(actual):
    """Facade for creating expectation objects.

    This will eventually create a specialised expectation object
    based on the class type."""

    return _registry.expect(actual)
        
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

