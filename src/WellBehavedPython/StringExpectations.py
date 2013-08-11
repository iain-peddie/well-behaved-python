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

class StringExpectations(DefaultExpectations):
    
    def toStartWith(self, expectedStart, userMessage = ''):
        message = self.buildMessage("to be a string starting with ", expectedStart, userMessage)
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

    def toEndWith(self, expectedEnd, userMessage = ''):
        message = self.buildMessage("to be a string ending with ", expectedEnd, userMessage)
        if len(expectedEnd) > len(self.actual):
            message += ", but it was too short"
            self.fail(message)
            return
        if self.actual.endswith(expectedEnd):
            self.success(message)
        else:
            message = self._diffStrings(self.actual, expectedEnd, message)
            self.fail(message)
    
    def toContain(self, expectedContents, userMessage = ''):
        message = self.buildMessage("to be a string containing ", expectedContents, userMessage)
        if self.actual.find(expectedContents) > -1:
            self.success(message)
        else:        
            self.fail(message)
            self.fail(message)
    def _diffStrings(self, a, b, originalMessage):
        from WellBehavedPython.api import expect
        aList = a.split('\n');
        bList = b.split('\n')
        expect(aList).toBeAnInstanceOf(list)
        expect(bList).toBeAnInstanceOf(list)
        generator = difflib.ndiff(aList, bList)
        message = originalMessage + "\nDifference is:"
        for line in generator:
            message += '\n'
            message += line
        return message
