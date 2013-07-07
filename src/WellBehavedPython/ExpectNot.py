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

from .BaseExpect import BaseExpect

class ExpectNot(BaseExpect):
    """Class used to indicate the opposite of expected outcomes."""

    def __init__(self, actual):
        BaseExpect.__init__(self, actual)

    def buildMessage(self, operation, expected, userMessage):
        """Builds the message passed to success and failure handling
        methods."""
        return self._buildMessage("not " + operation, expected, userMessage)

    def fail(self, Message = ""):
        """Indicate a failure.
        
        not fail should have the semantics of success."""
        pass

    def success(self, Message = ""):
        """Opposite semantincs to fail. Would be pass if pass was not a 
        reserved keyword.

        Not success is actually a failure contition. This should have the
        same semantics as Expect.fail()"""
        raise AssertionError(Message)

