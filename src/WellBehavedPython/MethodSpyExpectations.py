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
from .BaseExpect import BaseExpect
from .MethodSpy import MethodSpy

class MethodSpyExpectations(DefaultExpectations):

    def __init__(self, actual, strategy, reverseExpecter = None):
        """Constructor

        Inputs
        ------
        actual : the actual value to be compared against.
        strategy: the strategy to take on pass or fail methods
        reverseExpecter (optional) : an expecter that has the opposite semantics.
                  BaseExpect will store this in the Not field, allowing expect(a).Not...
                  to behave in the obvious way.
        """

        self.spy = actual
        DefaultExpectations.__init__(self, actual, strategy, reverseExpecter)

    def formatForMessage(self, instance):
        if isinstance(instance, MethodSpy):
            return instance.getDescription()
        print ("instance type is {}".format(type(instance)))
        return BaseExpect.formatForMessage(self, instance)

    def toHaveBeenCalled(self, userMessage = None, times = None):
        
        message = self.buildMessage("to have been called", None, userMessage)
        if times is None:
            self._toHaveBeenCalledOnce(message)
        else:
            if times == 1:
                pluralSuffix = ""
            else:
                pluralSuffix = "s"
            message = message + " {} time{}".format(times, pluralSuffix)
            self._toHaveBeenCalledNTimes(times, message)

    def _toHaveBeenCalledNTimes(self, times, message):
        if self.spy.getNumberOfCalls() == times:
            pass
        else:
            self.fail(message)

    def _toHaveBeenCalledOnce(self, message):
        if self.spy.hasBeenCalled():
            self.success(message)
        else:
            self.fail(message)
