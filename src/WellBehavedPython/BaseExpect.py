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

class BaseExpect:
    
    def __init__(self, actual):
        self.actual = actual

    def toEqual(self, expected):
        self.compareTypes(expected)
        message = self.buildMessage("to equal", expected);
        if self.actual == expected:
            self.success(message)
        else:        
            self.fail(message)

    def compareTypes(self, expected):
        
        # We want to compare types first. We also want this to
        # bypass the usual overriding of type comparison semantics.
        # Otherwise Expect(5).Not.toBeGreaterThan("6") will pass, when
        # it should really fail not (5 > "6") would throw an exception
        # and we should keep the same sematics here.

        actualType = type(self.actual)
        expectedType = type(expected)

        message = "Cannot compare instance of {} to instance of {} because their types differ".format(
            actualType, expectedType)
        assert actualType == expectedType, message

    def formatForMessage(self, unformatted):
        """Perform formatting for special types which need to be formatted
        differently, e.g. strings to indicate where their start and ends are."""
        if isinstance(unformatted, str):
            return "'{}'".format(unformatted)
        return unformatted

