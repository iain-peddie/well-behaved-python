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

class TestResult:
    """Stores all the data about an individual test result."""

    def __init__(self, suiteName, testName):
        self.SuiteName = suiteName
        self.TestName = testName
        self.StartTime = None
        self.EndTime = None

    def registerTestStarted(self):
        self.StartTime = datetime.now();

    def registerTestPassed(self):
        self.registerTestFinished("passed")

    def registerTestIgnored(self):
        self.registerTestFinished("ignored")
            
    def registerTestFailed(self, stackTrace):
        self.registerTestFinished("failed")

    def registerTestError(self, stackTrace):
        self.registerTestFinished("error")

    def registerTestFinished(self, finishType):
        message = "Unstarted test registered as {}".format(finishType)
        
        assert self._testStarted(), message

        self.EndTime = datetime.now()

    def _testStarted(self):
        if self.TestName == "beforeClass" or self.TestName == "afterClass":
            return True
        return self.StartTime is not None

    def getDuration(self):
        return self.EndTime - self.StartTime
