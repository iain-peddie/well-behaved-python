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


from datetime import timedelta
import traceback

from .TestResult import TestResult


class TestResults:
    """Class containing the results of a test run.

    A test run may be an individual test, or the results of runinng
    multiple tests through a suite."""

    def __init__(self):
        """Constructor."""
        self.testCount = 0
        self.failCount = 0
        self.passCount = 0
        self.errorCount = 0
        self.ignoredCount = 0
        self.stackTraces = []
        self.individualResults = []
        self.suiteResults = []

    def registerSuiteStarted(self, suiteName):
        childResults = TestResults()
        self.suiteResults.append(childResults)
        return childResults

    def registerSuiteCompleted(self, suiteName):
        pass

    def registerTestStarted(self, suiteName, testName):
        """Register the fact that a test started running."""        
        self.testCount += 1
        result = TestResult(suiteName, testName)
        result.registerTestStarted()
        self.individualResults.append(result)
        return result

    def registerTestFailed(self, suiteName, testName, stackTrace):
        """Register the fact that a test failed."""
        self.stackTraces.extend(stackTrace)
        self.failCount += 1
        result = self._getTestResult(suiteName, testName)
        result.registerTestFailed(stackTrace)

    def registerTestError(self, suiteName, testName, stackTrace, numErrors = 1):
        """Register the fact that a tet failed.
        
        Parameters
        ----------
        stackTrace : list of strings forming the stack trace for this error."""
        self.stackTraces.extend(stackTrace)
        self.errorCount += numErrors
        result = self._getTestResult(suiteName, testName)
        result.registerTestError(stackTrace)

    def registerTestPassed(self, suiteName, testName):
        """Register the fact that a test passed."""
        self.passCount += 1
        result = self._getTestResult(suiteName, testName)
        result.registerTestPassed()

    def registerTestIgnored(self, suiteName, testName):
        """Register the fact that a test was ignored."""
        self.ignoredCount += 1
        result = self._getTestResult(suiteName, testName)
        result.registerTestIgnored()

    def countTests(self):
        total = self.testCount
        for results in self.suiteResults:
            total += results.countTests()
        return total

    def countPasses(self):
        total = self.passCount
        for results in self.suiteResults:
            total += results.countPasses()
        return total

    def countFailures(self):
        total = self.failCount
        for results in self.suiteResults:
            total += results.countFailures()
        return total

    def countErrors(self):
        total = self.errorCount
        for results in self.suiteResults:
            total += results.countErrors()
        return total

    def countIgnores(self):
        total = self.ignoredCount
        for results in self.suiteResults:
            total += results.countIgnores()
        return total

    def getStackTraces(self):
        allTraces = self.stackTraces[:]
        for results in self.suiteResults:
            allTraces.extend(results.getStackTraces())
        return allTraces
    
    def summary(self):
        """Build a summary of the tests.

        This will construct a string describing the overall results
        of the test."""
        failedPart = self.buildMessagePart("failure", self.countFailures())
        errorPart = self.buildMessagePart("error", self.errorCount)
        ignoredPart = self.buildMessagePart("ignored", self.ignoredCount, False)
        testPart = self.buildMessagePart("test", self.testCount)
        
        line0 = "{} {} {} from {} in {}s\n".format(
            failedPart, errorPart, ignoredPart, testPart, 
            self.getDuration().total_seconds())
        lines = [line0]
        if len(self.stackTraces) > 0:
            lines.extend(self.stackTraces)
        return "".join(lines)

    def buildMessagePart(self, word, number, pluraliseFlag = True):
        return "{} {}{}".format(
            number, 
            word,
            self.pluralise(number, pluraliseFlag))

    def getDuration(self):
        totalDuration = timedelta()
        for result in self.individualResults:
            totalDuration += result.getDuration()
        for suite in self.suiteResults:
            totalDuration += suite.getDuration()
        return totalDuration

    def pluralise(self, count, pluraliseFlag = True):        
        if (count != 1 and pluraliseFlag):
            plural = "s"
        else:
            plural = ""
        
        return plural
        
    def _getTestResult(self, suiteName, testName):
        # TODO : check the result
        result = self.individualResults[-1]
        return result

