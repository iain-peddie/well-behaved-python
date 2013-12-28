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

from .DefaultExpectations import DefaultExpectations

import difflib
import re

class StringExpectations(DefaultExpectations):
    
    def toEqual(self, expected):
        """Compares the actual value to the expected value

        Asserts that the actual value stored in the object is equal 
        to the expected value.

        Inputs
        ------
        expected : the value that the actual value is expected to equal

        Exceptions
        ----------
        AssertionError : raised if self.actual does not equal expected, in which
                         case a diff of the strings is appended to the exception
                         message
"""
        self._compareTypes(expected)
        message = self.buildMessage("to equal ", expected, self.userMessage)
        if self.actual == expected:
            self.success(message)
        else:
            message = self._diffStrings(self.actual, expected, message)
            self.fail(message)

    def toStartWith(self, expectedStart):
        """Compares the actual value to the expected value

        Asserts that the text of the string starts with the
        expected start.

        Inputs
        ------
        expectedStart : the value that the actual text is expected
                        to start with

        Exceptions
        ----------
        AssertionError : raised if self.actual does not equal expected.
"""

        message = self.buildMessage("to be a string starting with ", expectedStart, self.userMessage)
        if len(expectedStart) > len(self.actual):
            message += ", but it was too short"
            self.fail(message)
            return
        truncatedActual = self.actual[0:len(expectedStart)]
        if self.actual.startswith(expectedStart):
            self.success(message)
        else:
            message = self._diffStrings(self.actual, expectedStart, message)
            self.fail(message)

    def toEndWith(self, expectedEnd):
        """Compares the actual value to the expected value

        Asserts that the text of the string ends with the
        expected end.

        Inputs
        ------
        expectedEnd : the value that the actual text is expected
                      to end with

        Exceptions
        ----------
        AssertionError : raised if self.actual does not equal expected.
"""

        message = self.buildMessage("to be a string ending with ", expectedEnd, self.userMessage)
        if len(expectedEnd) > len(self.actual):
            message += ", but it was too short"
            self.fail(message)
            return
        if self.actual.endswith(expectedEnd):
            self.success(message)
        else:
            message = self._diffStrings(self.actual, expectedEnd, message)
            self.fail(message)
    
    def toContain(self, expectedContents):
        """Compares the actual text to the expected contents

        Asserts that the text of the string containsh the
        expected contents.

        Inputs
        ------
        expectedConetnts : the value that the actual text is expected
                           to contain

        Exceptions
        ----------
        AssertionError : raised if self.actual does not equal expected.
"""

        message = self.buildMessage("to be a string containing ", expectedContents, self.userMessage)
        if self.actual.find(expectedContents) > -1:
            self.success(message)
        else:        
            self.fail(message)


    def toMatch(self, pattern):
        """Compares the actual value to the pattern

        Asserts that the actual value matches the given regular expression
        pattern anywhere.

        Inputs
        ------
        pattern: The string or compiled regular expression pattern that the
                 actual value is epxected to match

        Exceptions
        ----------
        AssertionError : raised if self.actual does not match pattern.
"""
        if type(pattern) == str:
            pattern = re.compile(pattern)
        message = self.buildMessage("to be a string matching regular expression pattern ",
                                    pattern.pattern, self.userMessage)

        if pattern.search(self.actual):
            self.success(message)
        else:
            self.fail(message)

    def _diffStrings(self, a, b, originalMessage):
        """Compares the conents of two strins
        
        Compares the contents of two strings, generates a difference
        between them, and appends that to the message passed in
        as originalMessage

        Inputs
        ------
        a : the first string
        b : the second string
        originalMessage: the original message before the string content difference
                         is added

        Returns
        -------
        A message with the contents of orignalMessage followed by a summary of
        the differnece between the two strings."""
        from WellBehavedPython.api import expect
        aList = a.split('\n');
        bList = b.split('\n')
        generator = difflib.ndiff(aList, bList)
        message = originalMessage + "\nDifference is:"
        for line in generator:
            message += '\n'
            message += line
        return message
