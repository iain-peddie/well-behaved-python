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
    """A class for replacing methods with for decoupling tests.

    Most users should not create these directly, but instead use the
    spyOn(object.method) syntax, which both creates the method spy and
    replaces the object's method with the spy. 

    Once created and installed, a spy will record each call made to the
    original method. Optionally, it can also do any of the following:
      - return a given value. Useful if this is being used by a system under test,
        which will fail if None is returned as the value to the method
      - raise an exception. Useful for unhappy path testing. This converts
        the spy from being a TestSpy into a TestSaboteur.
      - call through to the original method. This can be useful for writing
        integration tests which check that the system under test calls through
        to it's partern instances correctly."""

    def __init__(self, methodName = "anonymous", methodObject = None):
        self.methodName = methodName
        self.methodObject = methodObject
        self.callArguments = []
        self.keywordCallArguments = []
        self.returnValue = None
        self.returnValueSet = False
        self.exceptionClass = None
        self.callThrough = False


    def __call__(self, *args, **keywordArgs):
        """Call method. 

        This turns the object into a function object, which allows it to replace
        methods on objects. It also records the state. It takes a fully abrtitary
        set of arguments by having both optional positional arguments and optional
        keyword arguments."""

        result = None

        self._recordCallArguments(args, keywordArgs)
        result = self._callThroughIfNecessary(result, args, keywordArgs)
        self._raiseExceptionIfNecessary()
        result = self._overrideReturnValueIfNecessary(result)

        return result

    def andReturn(self, returnValue):
        """Sets the return value when the method is called.

        Inputs
        ------
        returnValue: the value to return when the spy is called."""        

        self.returnValue = returnValue
        self.returnValueSet = True
        return self

    def andRaise(self, exceptionClass):
        """Sets an exception class to throw an instance of when called.

        Inputs
        ------
        exceptionClass : the class to instantiate. It is expected that this can be called with
                         a string argument."""
        self.exceptionClass = exceptionClass
        return self

    def andCallThrough(self):
        """Indicates that the original method should be called."""
        self.callThrough = True
        return self

    def andCall(self, replacementMethod):
        """Replaces the target method, and sets the call through flag.
        
        Inputs
        ------
        replacementMethod: An item which is callable, and is called when this method spy is."""

        self.methodObject = replacementMethod
        self.callThrough = True
        return self

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

    def generateCallReport(self, specialCallIndex = None):
        """Generates a report of the number of call arguments, and what they were.

        This report uses format for arguments. If the report for custom types is
        badly formed, consider writing or updating the __repr__ method.

        Inputs
        ------
        specialCallIndex : the call index to be marked out as special

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
            keywordArgs = self.keywordCallArguments[callIndex]
            if callIndex == specialCallIndex:
                report += "=> "
            report += self.formatCallArguments(args, keywordArgs) + "\n"

        return report

    def formatCallArguments(self, positionalArguments = None, keywordArguments = None):
        """Formats call arguments in a standard, hopefully sensible way.

        Inputs
        ------
        positionalArguments : expected to be a tuple containing the
                              arguments specified by position.
        keywordArguments : expected to be a dictionary containing keyword value pairs"""
        

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

    def _recordCallArguments(self, args, keywordArgs):
        self.callArguments.append((args))
        self.keywordCallArguments.append(keywordArgs)

    def _callThroughIfNecessary(self, result, args, keywordArgs):
        if self.callThrough:
            result = self.methodObject(*args, **keywordArgs)
        return result

    def _raiseExceptionIfNecessary(self):
        if self.exceptionClass is not None:
            instance = self.exceptionClass('generated by method spy {}'.format(self.methodName))
        else:
            instance = None

        if instance is not None:
            raise(instance)

    def _overrideReturnValueIfNecessary(self, result):
        if self.returnValueSet:
            result = self.returnValue
        return result

