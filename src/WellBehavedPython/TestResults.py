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


from datetime import *
import traceback

class TestResults:
    """Class containing the results of a test run.

    A test run may be an individual test, or the results of runinng
    multiple tests through a suite."""

    def __init__(self, name = "<anonymous>"):
        """Constructor."""
        self.name = name
        self._testCount = 0
        self._failCount = 0
        self._passCount = 0
        self._errorCount = 0
        self._ignoredCount = 0
        self.stackTraces = []
        self.suiteResults = []
        self.suiteStack = []
        self.activeResults = self
        self.startTime = None
        self.endTime = None

    def registerSuiteStarted(self, suiteName):
        self._pushActiveResults(suiteName)
        return self.activeResults

    def registerSuiteCompleted(self, suiteName):
        self._popActiveResults()        

    def registerTestStarted(self, suiteName, testName):
        self._pushActiveResults(testName)
        return self.activeResults._registerTestStarted(suiteName, testName)

    def registerTestPassed(self, suiteName, testName):
        self.activeResults._registerTestPassed(suiteName, testName)
        self._popActiveResults()

    def registerTestFailed(self, suiteName, testName, stackTrace):
        self.activeResults._registerTestFailed(suiteName, testName, stackTrace)
        self._popActiveResults()

    def registerTestError(self, suiteName, testName, stackTrace, numErrors = 1):
        self.activeResults._registerTestError(suiteName, testName, stackTrace, numErrors)
        if testName not in ("beforeClass", "afterClass"):
            self._popActiveResults()

    def registerTestIgnored(self, suiteName, testName):
        self.activeResults._registerTestIgnored(suiteName, testName)
        self._popActiveResults()

    def countTests(self):
        total = self._testCount
        for results in self.suiteResults:
            total += results.countTests()
        return total

    def countPasses(self):
        total = self._passCount
        for results in self.suiteResults:
            total += results.countPasses()
        return total

    def countFailures(self):
        total = self._failCount
        for results in self.suiteResults:
            total += results.countFailures()
        return total

    def countErrors(self):
        total = self._errorCount
        for results in self.suiteResults:
            total += results.countErrors()
        return total

    def countIgnored(self):
        total = self._ignoredCount
        for results in self.suiteResults:
            total += results.countIgnored()
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
        errorPart = self.buildMessagePart("error", self.countErrors())
        ignoredPart = self.buildMessagePart("ignored", self.countIgnored(), False)
        testPart = self.buildMessagePart("test", self.countTests())
        
        line0 = "{} {} {} from {} in {}s\n".format(
            failedPart, errorPart, ignoredPart, testPart, 
            self.getDuration().total_seconds())
        lines = [line0]
        stackTraces = self.getStackTraces()
        if len(stackTraces) > 0:
            lines.extend(stackTraces)
        return "".join(lines)

    def buildMessagePart(self, word, number, pluraliseFlag = True):
        return "{} {}{}".format(
            number, 
            word,
            self.pluralise(number, pluraliseFlag))

    def getDuration(self):
        if self.endTime is None and self.startTime is None:
            totalDuration = timedelta()
        else:
            totalDuration = self.endTime - self.startTime #timedelta()
        for suite in self.suiteResults:
            totalDuration += suite.getDuration()
        return totalDuration

    def pluralise(self, count, pluraliseFlag = True):        
        if (count != 1 and pluraliseFlag):
            plural = "s"
        else:
            plural = ""
        
        return plural
        
    def _pushActiveResults(self, name):
        self.suiteStack.append(self.activeResults)
        results = TestResults(name);
        self.activeResults.suiteResults.append(results)
        self.activeResults = results

    def _popActiveResults(self):
        self.activeResults = self.suiteStack.pop()

    def _registerTestStarted(self, suiteName, testName):
        """Register the fact that a test started running."""
        
        self._testCount += 1
        self.startTime = datetime.now()
        return self

    def _registerTestPassed(self, suiteName, testName):
        """Register the fact that a test passed."""
        self._passCount += 1
        self._registerTestFinished(suiteName, testName)

    def _registerTestFailed(self, suiteName, testName, stackTrace):
        """Register the fact that a test failed."""
        self.stackTraces.extend(stackTrace)
        self._failCount += 1
        self._registerTestFinished(suiteName, testName)

    def _registerTestIgnored(self, suiteName, testName):
        """Register the fact that a test was ignored."""
        self._ignoredCount += 1
        self._registerTestFinished(suiteName, testName)

    def _registerTestError(self, suiteName, testName, stackTrace, numErrors = 1):
        """Register the fact that a test failed.
        
        Parameters
        ----------
        stackTrace : list of strings forming the stack trace for this error."""
        self.stackTraces.extend(stackTrace)
        self._errorCount += numErrors
        self._registerTestFinished(suiteName, testName)

    def _registerTestFinished(self, suiteName, testName):
        self.endTime = datetime.now()

    def __repr__(self):
        return """TestResults : {}
Direct:
------
tests       {}
pass        {}
fail        {}
error       {}
ignore      {}
stackTrace  {}

Overall
-------
tests       {}
pass        {}
fail        {}
error       {}
ignore      {}
stackTrace  {}""".format(self.name,
                         self._testCount,
                         self._passCount,
                         self._failCount,
                         self._errorCount,
                         self._ignoredCount,
                         self.stackTraces,
                         self.countTests(),
                         self.countPasses(),
                         self.countFailures(),
                         self.countErrors(),
                         self.countIgnored(),
                         self.getStackTraces())
                        

