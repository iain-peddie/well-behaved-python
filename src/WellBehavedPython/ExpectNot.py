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

class ExpectNot:
    """Class used to indicate the opposite of expected outcomes."""

    def __init__(self):
        """Constructor

        Inputs
        ------
        actual : the actual value to be compared against.
        """

    def fail(self, message = ""):
        """Indicate a failure, or handle a failed comparison operation.

        ExpectNot has the opposite semantics to expect, that is a failure
        behaves like a success and a success behaves like a failure.

        Inputs
        ------
        message(optional) : ignored. Part of the BaseExpect interface.
        """
        
        #not fail should have the semantics of success
        pass

    def success(self, Message = ""):
        """Indicate a success, or handle a succesful comparison operation.

        ExpectNot has the opposite semantics to expect, that is a failure
        behaves like a success and a success behaves like a failure.

        Inputs
        ------
        message(optional) : Message to be passed to the raised AssertionError.
        """
        raise AssertionError(Message)

    def decorateOperation(self, operation):
        return "not " + operation


