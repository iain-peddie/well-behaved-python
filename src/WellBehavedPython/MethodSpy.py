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

class MethodSpy:

    def __init__(self, methodName = "anonymous"):
        self.methodName = methodName
        self.callArguments = []
        self.keywordCallArguments = []

    def __call__(self, *args, **keywordArgs):
        self.callArguments.append((args))
        self.keywordCallArguments.append(keywordArgs)

    def getDescription(self):
        """Gets a description of this method spy.

        Returns
        -------
        The description fo this method spy        
        """
        return "<{}>".format(self.methodName)

    def getNumberOfCalls(self):
        """Gets the number of times this method spy has been called.

        Returns
        -------
        The number of times this method spy has been called."""
        return len(self.callArguments)

    def hasBeenCalled(self):
        """Gets whether the spy has been called at all.

        Returns
        -------
        True, if the spy has been called
        False otherwise."""
        return len(self.callArguments) > 0

    def hasBeenCalledWith(self, expectedArgs = (), expectedKeywordArgs = {}, callIndex = None):
        """Gets whether the spy has been called with the given arguments.

        Either returns whether the given arguments match any call, or whether
        the callIndexth call matches the expected arguments.

        Inputs
        ------
        expectedArgs : the expected input arguments
        callIndex: The index of the call to compare against a specific
                   call, or None to compare against all calls."""

        if callIndex is not None:
            return (self.callArguments[callIndex] == expectedArgs and
                    self.keywordCallArguments[callIndex] == expectedKeywordArgs)
        else:
            return (expectedArgs in self.callArguments and
                    expectedKeywordArgs in self.keywordCallArguments)

    def generateCallReport(self):
        """Generates a report of the number of call arguments, and what they were.

        This report uses format for arguments. If the report for custom types is
        badly formed, consider writing or updating the __repr__ method.

        Returns
        -------
        A string containing the call arguments all on a single line, where possible.
        The report for one call will span multiple lines if the standard representation
        of the argument contains newlines. There is little that can be done about that,
        without overriding the standard type formatting, which does not seem to be sensible
        behavior."""

        report = ""
        if len(self.callArguments) == 0:
           return report 
        for callIndex in range(0, len(self.callArguments)):
            args = self.callArguments[callIndex]
            report += self.formatCallArguments(args) + "\n"

        return report

    def formatCallArguments(self, positionalArguments = None, keywordArguments = None):
        """Formats call arguments in a standard, hopefully sensible way.

        Inputs
        ------
        positionalArguments : expected to be a tuple containing the
                              arguments specified by position.
        keywordArguments : expected to be a dictionary containing keyword value pairs"""
        

        # TODO : this method is still in progress, and needs to be
        # TODO : completed

        if positionalArguments is None:
            positionalArguments = ()
        if keywordArguments is None:
            keywordArguments = {}
                
        formatted = "("
        delimiter = ""
        
        for arg in positionalArguments:
            formattedArg = self._formatArgument(arg)
            formatted = "{}{}{}".format(formatted, delimiter, formattedArg)
            delimiter = ", "

        keywords = list(keywordArguments.keys())
        keywords.sort()

        for argName in keywords:
            argValue = self._formatArgument(keywordArguments[argName])
            formatted = "{}{}{}={}".format(formatted, delimiter, argName, argValue)
            delimiter = ", "
            
        formatted = "{})".format(formatted)
        return formatted

    def _formatArgument(self, arg):
        if isinstance(arg, str):
            formattedArg = "'{}'".format(arg)
        else:
            formattedArg = arg
        return formattedArg

