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

import traceback

class TestResults:
    """Class containing the results of a test run.

    A test run may be an individual test, or the results of runinng
    multiple tests through a suite."""

    def __init__(self):
        """Constructor."""
        self.testCount = 0
        self.failCount = 0
        self.passCount = 0
        self.stackTraces = []

    def registerTestStarted(self):
        """Register the fact that a test started running."""
        self.testCount += 1

    def registerTestFailed(self, stackTrace):
        """Register the fact that a test failed."""
        self.stackTraces.extend(stackTrace)
        self.failCount += 1

    def registerTestPassed(self):
        """Register the fact that a test passed."""
        self.passCount += 1
    
    def summary(self):
        """Build a summary of the tests.

        This will construct a string describing the overall results
        of the test."""
        plural = self.pluralise(self.testCount)
        line0 = "{} failed from {} test{}\n".format(
            self.failCount, self.testCount, plural)
        lines = [line0]
        if len(self.stackTraces) > 0:
            lines.extend(self.stackTraces)
        return "".join(lines)

    def pluralise(self, count):
        if count != 1:
            plural = "s"
        else:
            plural = ""
        
        return plural
        
