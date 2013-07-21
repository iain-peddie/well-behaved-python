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
from .NumericExpectations import *

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

    if isinstance(actual, float) or isinstance(actual, int):
        reverser = NumericExpectations(actual, reverseStrategy)
        return NumericExpectations(actual, strategy, reverser)
    else:
        reverser = DefaultExpectations(actual, reverseStrategy)
        return DefaultExpectations(actual, strategy, reverser)    


