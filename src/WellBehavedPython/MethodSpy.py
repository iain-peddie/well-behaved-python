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

class MethodSpy:

    def __init__(self, methodName = "anonymous"):
        self.methodName = methodName
        self.callArguments = []

    def __call__(self, *args):
        self.callArguments.append((args))

    def getDescription(self):
        """Gets a description of this method spy.

        Returns
        -------
        The description fo this method spy        
        """
        return "<{}>".format(self.methodName)

    def getNumberOfCalls(self):
        """Gets the number of times this method spy has been called.

        Returns
        -------
        The number of times this method spy has been called."""
        return len(self.callArguments)

    def hasBeenCalled(self):
        """Gets whether the spy has been called at all.

        Returns
        -------
        True, if the spy has been called
        False otherwise."""
        return len(self.callArguments) > 0

    def hasBeenCalledWith(self, expectedArgs, callIndex = 0):
        """Gets whether the spy has been called with the given arguments.

        Either returns whether the given arguments match any call, or whether
        the callIndexth call matches the expected arguments.

        Inputs
        ------
        expectedArgs : the expected input arguments
        callIndex: The index of the call to compare against a specific
                   call, or None to compare against all calls."""

        if callIndex is not None:
            return self.callArguments[callIndex] == expectedArgs
        else:
            return expectedArgs in self.callArguments
