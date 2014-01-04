#!/usr/bin/env python3

# Copyright 2013-4 Iain Peddie inr314159@hotmail.com
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
from ..Fakes.MethodSpy import MethodSpy

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
        self.callIndex = None
        DefaultExpectations.__init__(self, actual, strategy, reverseExpecter)

    def formatForMessage(self, instance):
        """Formats instance for insertion into a message

        Inputs
        ------
        instance : the instance of an object to format for a message."""

        if isinstance(instance, MethodSpy):
            return instance.getDescription()
        return BaseExpect.formatForMessage(self, instance)

    def forCallNumber(self, callNumber):
        """Indicates to only look at a certain call.

        Inputs
        ------
        callNumber: the call number to examine."""

        self.callIndex = callNumber - 1
        if self.Not is not None:
            self.Not.forCallNumber(callNumber)
        return self

    def _numberTimesString(self, times):
        if times == 1:
            pluralSuffix = ""
        else:
            pluralSuffix = "s"
        return "{} time{}".format(times, pluralSuffix)

    def toHaveBeenCalled(self):        
        """Performs the specific logic of the expectation that a method has been called.
        """
        
        message = self.buildMessage("to have been called", None)
        if self.spy.hasBeenCalled():
            self.success(message)
        else:
            self.fail(message)

        return self

    def toHaveBeenCalledExactly(self, expectedTimes):
        """Logic to assert that the spy has been called exactly expectedTimes times.

        Inputs
        ------
        expectedTimes : the number of times the spy is expected to have been called.
"""
        message = self._buildMethodSpyMessage("exactly", expectedTimes)

        if self.spy.getNumberOfCalls() == expectedTimes:
            self.success(message)
        else:
            self.fail(message)

        return self

    def toHaveBeenCalledAtLeast(self, expectedTimes):
        """Logic to asser the spy has been called at least expectedTimes

        Inputs
        ------
        expectedTimes : the number of calls the spy should beat or match."""

        message = self._buildMethodSpyMessage("at least", expectedTimes)

        actualTimes = self.spy.getNumberOfCalls()

        if actualTimes >= expectedTimes:
            self.success(message)
        else:
            self.fail(message)
        return self

    def toHaveBeenCalledAtMost(self, expectedTimes):
        """Logic to asser the spy has been called at least expectedTimes

        Inputs
        ------
        expectedTimes : the number of calls the spy should be under or match."""

        message = self._buildMethodSpyMessage("at most", expectedTimes)

        actualTimes = self.spy.getNumberOfCalls()
        
        if actualTimes <= expectedTimes:
            self.success(message)
        else:
            self.fail(message)

        return self

    def _buildMethodSpyMessage(self, comparisonWord, expectedTimes):
        baseMessage = "to have been called {} {}".format(comparisonWord, 
                                                         self._numberTimesString(expectedTimes))
        extra = self._buildCalledTimesSubmessage()
        return self.buildMessage(baseMessage, None, extra = extra)

    def _buildCalledTimesSubmessage(self):
        actualTimes = self.spy.getNumberOfCalls()
        if self.spy.hasBeenCalled():
            submessage = ", but it was called {}.".format(self._numberTimesString(actualTimes))
        else:
            submessage = ", but it was never called."
        return submessage


    def toHaveBeenCalledWith(self, *args, **keywordArgs):
        """Expects that the spy was called with a set of arguments matching the given set

        Note
        ----
        This syntax differs from most assertions, in that the options to this are set outside
        of this call. In order for them to appear, they would have to be between the optional
        positional arugments and the optional keyword arguments, and this would be confusing.

        Furthermore, it would constrain spied methods to not have keyword arguments of
        callIndex or userMessage. These seem sufficiently generic variable names that blocking 
        their use would be constraining, with no particular benefit.

        To set the userMessage, callIndex or both, use the syntax:
        expect(yourSpy).withUserMessage(message).toHaveBeenCalledWith(...)
        expect(yourSpy).forCallNumber(2).toHaveBeenCalledWith(...)

        The two methods both return self, so can be chained tother:
        
        expect(yourSpy).withUserMessage(message).forCallNumber(3).toHaveBeenCalledWith().

        Inputs
        ------
        *args : optional positional arguments
        **keywordsArguments : optional keyword arguments

        args and keywordArgs combine to allow this method to be called with an arbritary
        set of arguments, which is needed to allow it to act as an assertion without constraint
        for method calls."""
        
        reason = "to have been called with {}".format(self.spy.formatCallArguments(args, keywordArgs));
        if not self.spy.hasBeenCalled():
            message = self.buildMessage(reason, None, self.userMessage, extra = ", but it was not called")
            self.fail(message)

        if self.callIndex is None:
            extra = ", but it was called {} with:\n{}".format(
                self._numberTimesString(
                    self.spy.getNumberOfCalls()), 
                self.spy.generateCallReport())
        else:
            extra = " on the {} call, but it was called with:\n{}".format(
                self._numberToPositionString(self.callIndex + 1),
                self.spy.generateCallReport(self.callIndex))
        message = self.buildMessage(reason, None, self.userMessage, extra = extra)
        
        if self.spy.hasBeenCalledWith(args, keywordArgs, self.callIndex):
            self.success(message)
        else:
            self.fail(message)

    def time(self):
        """Do nothing method.

        This method exists as syntactic sugar to allow the readable phrase expect(spy).toHaveBeenCalledXXX(1).time() 
        with XXX being one of AtLeast, AtMost or Exactly.

        Returns
        -------
        self : this allows more function calls to be chained allowing for a fluent syntax of expressions."""
        return self

    def times(self):
        """Do nothing method.

        This method exists as syntactic sugar to allow the readable phrase expect(spy).toHaveBeenCalledXXX(2).times() 
        with XXX being one of AtLeast, AtMost or Exactly.

        Returns
        -------
        self : this allows more function calls to be chained allowing for a fluent syntax of expressions."""
        return self
        


    def _numberToPositionString(self, number):
        suffixes = { 1: "st", 
                     2: "nd", 
                     3: "rd"}
        
        if number in suffixes.keys():
            suffix = suffixes[number]
        else:
            suffix = "th"

        return "{}{}".format(number, suffix)


