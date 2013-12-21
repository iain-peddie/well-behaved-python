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
            message = message + " " + self._numberTimesString(times)
            self._toHaveBeenCalledNTimes(times, message)

    def _numberTimesString(self, times):
        if times == 1:
            pluralSuffix = ""
        else:
            pluralSuffix = "s"
        return "{} time{}".format(times, pluralSuffix)            

    def toHaveBeenCalledWith(self, *args):
        reason = "to have been called with {}".format(self.spy.formatCallArguments(args));
        if not self.spy.hasBeenCalled():
            message = self.buildMessage(reason, None, None, extra = ", but it was not called")
            self.fail(message)

        extra = ", but it was called {} with:\n{}".format(self._numberTimesString(
                self.spy.getNumberOfCalls()), 
                                                          self.spy.generateCallReport())
        message = self.buildMessage(reason, None, None, extra = extra)
        
        if self.spy.hasBeenCalledWith(args[:]):
            pass
        else:
            self.fail(message)

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
