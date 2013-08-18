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
import sys

class ConsoleTestRunner:
    """Runs tests and displays minimal output at the console.

    This behaves like the simple cosole test runners in JUnit etc,
    displaying a dot for a passed test, F for a failed test,
    E for a test that had an error, and I for an ignored test."""
    def __init__(self, output = sys.stdout):
        self._output = output
        self._resultsPerLine = 30
        self._currentResult = 0
        self.outputBuffer = io.StringIO()
#        sys.stdout = self.outputBuffer
#        sys.stderr = self.outputBuffer

    def __del__(self):
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

        self.results = TestResults()
        self._testCount = suite.countTests()
        self._output.write("Starting test run of {} test{}\n".format(
                self._testCount, self.results.pluralise(self._testCount)))
        suite.run(self)
        self._endResultsLineIfNecessary()
        self._output.write(self.results.summary())
        self._output.write("\n")
        self._output.write(self.outputBuffer.getvalue())

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

    def _endResultsLineIfNecessary(self):
        """End the results line if it is right to do so."""
        if (self._currentResult == self._testCount and
           self._currentResult > 0):
            self._output.write("\n")

    def _writeResult(self, result):
        """Write a single result to the output."""
        self._output.write(result)
        self._currentResult += 1
