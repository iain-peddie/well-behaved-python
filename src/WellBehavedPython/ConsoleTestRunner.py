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

from .TestResults import TestResults

import io
import traceback
import sys

class ConsoleTestRunner:
    """Runs tests and displays minimal output at the console.

    This behaves like the simple cosole test runners in JUnit etc,
    displaying a dot for a passed test, F for a failed test,
    E for a test that had an error, and I for an ignored test."""
    def __init__(self, output = sys.stdout, resultsPerLine = 30, bufferOutput = True):
        self._output = output
        self._resultsPerLine = resultsPerLine
        self._currentResult = 0
        self.outputBuffer = io.StringIO()
        self.bufferOutput = bufferOutput
        if self.bufferOutput:
            sys.stdout = self.outputBuffer
            sys.stderr = self.outputBuffer

    def __del__(self):
        if self.bufferOutput:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

    def run(self, suite):
        """Run the given test suite.

        Runs the given test suite, reporting results as the
        individual test results come in.

        Parameters
        ----------
        suite : A testable object, most probably a test suite.
        """
        try:
            self.results = TestResults()
            self._testCount = suite.countTests()
            self._output.write("Starting test run of {} test{}\n".format(
                self._testCount, self.results.pluralise(self._testCount)))
            suite.run(self)
            self._output.write(self.results.summary())
            self._output.write("\n")
            self._output.write(self.outputBuffer.getvalue())
        except Exception as ex:
            sys.__stdout__.write("Error running test suite:\n")
            traceback.print_exc(file = sys.__stdout__)

        return self.results

    def registerTestStarted(self):
        """Regsiter the start of a test."""
        self.results.registerTestStarted()

    def registerTestFailed(self, stackTrace):
        """Register a test failed."""
        self._writeResult("F")
        self.results.registerTestFailed(stackTrace)

    def registerTestPassed(self):
        """register a test passed."""
        self._writeResult(".")
        self.results.registerTestPassed()

    def registerTestError(self, stackTrace):
        """Register a test failed."""
        self._writeResult("E")
        self.results.registerTestError(stackTrace)

    def registerTestIgnored(self):
        """Register a test ignored."""
        self._writeResult("I")
        self.results.registerTestIgnored()

    def _endResultsLineIfNecessary(self):
        """End the results line if it is right to do so."""
        if (self._isEndOfLine() or self._isLastResult()): 
             self._output.write("\n")

    def _isLastResult(self):
        return (self._currentResult == self._testCount and
           self._currentResult > 0)

    def _isEndOfLine(self):        
        modulus =  self._currentResult % self._resultsPerLine
        return modulus == 0
        return moudulus
        

    def _writeResult(self, result):
        """Write a single result to the output."""
        self._output.write(result)
        self._currentResult += 1
        self._endResultsLineIfNecessary()
