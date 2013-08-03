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

from collections import Iterable
from collections import Mapping

_numericTypes = (int, float)
_containerTypes = (list, tuple, set, frozenset)

def isNumeric(actual):
    """Determine whether actual is a numeric type."""
    for nt in _numericTypes:
        if isinstance(actual, nt):
            return True

    return False

def isDictionary(actual):
    """Determine whether actual is a dictionary like type with keys and values."""
    return isinstance(actual, Mapping)

def isIterable(actual):
    # using isinstance Iterable allows new 'containers' to be
    # tested by registering with Iterable as in
    # Iterable.register(MyClass)
    return isinstance(actual, Iterable)

