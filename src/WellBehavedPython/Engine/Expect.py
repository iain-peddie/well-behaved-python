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

from ..Expectations.DefaultExpectations import DefaultExpectations
from .ExpectNot import ExpectNot

class Expect:
    """Class used to indicate expected outcomes."""

    def __init__(self):
        """Constructor

        Inputs
        ------
        actual : the actual value to be compared against.
        """

    def fail(self, Message = ""):
        """Indicate a failure, or handle a failed comparison operation.

        Inputs
        ------
        message(optional) : Message to be passed to the raised AssertionError.
        """
        raise AssertionError(Message)

    def success(self, Message = ""):
        """Indicate a success, or handle a succesful comparison operation.

        Inputs
        ------
        message(optional) : ignored. Part of the BaseExpect interface.
        """
        pass

    def decorateOperation(self, operation):
        """Add any extra text around the operation description string.

        This is used in the assertion message building code.

        Inputs
        ------
        operation: a text description of the operation being performed, eg. 'to equal'
        
        Returns
        -------
        An updated description of the operation being performed which is
        more consistent with this being the strategy, , e.g. 'to equal'."""
        return operation

