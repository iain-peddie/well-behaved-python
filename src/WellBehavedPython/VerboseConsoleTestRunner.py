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
from .ConsoleTestRunner import ConsoleTestRunner

import io
import traceback
import sys

class VerboseConsoleTestRunner(ConsoleTestRunner):
    """Runs tests and displays verbose output at the console.

    This behaves like the verbose cosole test runners in JUnit etc,
    displaying the name of a test and then the result and timing
    details."""
    def __init__(self, output = sys.stdout,  bufferOutput = True):
        ConsoleTestRunner.__init__(self, output, bufferOutput = bufferOutput)
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

    def registerSuiteStarted(self, suiteName):
        pass

    def registerSuiteCompleted(self, suiteName):
        pass

    def registerTestStarted(self, suiteName, testName):
        """Regsiter the start of a test."""        
        self._output.write(testName)
        self.lastResult = self.results.registerTestStarted(suiteName, testName)

    def registerTestFailed(self, suiteName, testName, stackTrace):
        """Register a test failed."""
        self.results.registerTestFailed(suiteName, testName, stackTrace)
        self.registerTestFinished(suiteName, testName, "failed")

    def registerTestPassed(self, suiteName, testName):
        """register a test passed."""
        self.results.registerTestPassed(suiteName, testName)
        self.registerTestFinished(suiteName, testName, "passed")

    def registerTestError(self, suiteName, testName, stackTrace):
        """Register a test failed."""
        self.results.registerTestError(suiteName, testName, stackTrace)
        self.registerTestFinished(suiteName, testName, "error")

    def registerTestIgnored(self, suiteName, testName):
        """Register a test ignored."""
        self.results.registerTestIgnored(suiteName, testName)
        self.registerTestFinished(suiteName, testName, "ignored")

    def registerTestFinished(self, suiteName, testName, stateMessage):
        time = self.lastResult.getDuration().total_seconds()
        self._output.write("... {} in {:f}s\n".format(stateMessage, time))


    
