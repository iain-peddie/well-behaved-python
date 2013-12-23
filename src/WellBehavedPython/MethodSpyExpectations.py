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
        self.userMessage = None
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

    def withUserMessage(self, userMessage):
        """Sets an extra message to be put into the failure message

        Inputs
        -----
        userMessage : The extra sub-message to put into the expectation failure message."""

        self.userMessage = userMessage
        if self.Not is not None:
            self.Not.withUserMessage(userMessage)
        return self

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

    def toHaveBeenCalled(self, times = None):        
        """Performs the specific logic of the expectation that a method has been called.

        Inputs
        ------
        times : can be:
                None, in which case the logic is has the method been called at all
                an integer, in which case the logic is has the mehtod been called exactly 'times' times.
        """
        
        message = self.buildMessage("to have been called", None, self.userMessage)
        if times is None:
            self._toHaveBeenCalledAtAll(message)
        else:
            message = message + " " + self._numberTimesString(times)
            self._toHaveBeenCalledNTimes(times, message)

    def toHaveBeenCalledAtLeast(self, expectedTimes):
        """Logic to asser the spy has been called at least expectedTimes

        Inputs
        ------
        expectedTimes : the number of calls the spy should beat or match."""
        baseMessage  = "to have been called at least {}".format(self._numberTimesString(expectedTimes))
        actualTimes = self.spy.getNumberOfCalls()

        if self.spy.hasBeenCalled():
            extra = ", but it was called {}.".format(self._numberTimesString(actualTimes))
        else:
            extra = ", but it was never called."
        message = self.buildMessage(baseMessage, None, self.userMessage, extra)
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
        return self

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

    def _toHaveBeenCalledNTimes(self, times, message):
        if self.spy.getNumberOfCalls() == times:
            self.success(message)
        else:
            self.fail(message)

    def _toHaveBeenCalledAtAll(self, message):
        if self.spy.hasBeenCalled():
            self.success(message)
        else:
            self.fail(message)
