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
from .ExpectNot import ExpectNot

class Expect(BaseExpect):
    """Class used to indicate expected outcomes."""

    def __init__(self, actual):
        BaseExpect.__init__(self, actual)
        self.Not = ExpectNot(actual)

    def buildMessage(self, operation, expected):
        """Build the message that will be put into the AssertionError
        if the condition fails. The message will contain the actual
        values, the expected value and the operation being performed."""
        formattedActual = self.formatForMessage(self.actual);
        formattedExpected = self.formatForMessage(expected)
        return "Expected {} {} {}".format(formattedActual, operation,
                                          formattedExpected)

    def formatForMessage(self, unformatted):
        """Perform formatting for special types which need to be formatted
        differently, e.g. strings to indicate where their start and ends are."""
        if isinstance(unformatted, str):
            return "'{}'".format(unformatted)
        return unformatted

    def fail(self, Message = ""):
        raise AssertionError(Message)

    def success(self, Message = ""):
        pass
