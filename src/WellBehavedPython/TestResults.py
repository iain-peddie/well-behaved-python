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

class TestResults:
    """Class containing the results of a test run.

    A test run may be an individual test, or the results of runinng
    multiple tests through a suite."""

    def __init__(self):
        """Constructor."""
        self.testCount = 0
        self.failCount = 0

    def registerTestStarted(self):
        """Register the fact that a test started running."""
        self.testCount += 1

    def registerTestFailed(self):
        """Register the fact that a test failed."""
        self.failCount += 1
    
    def summary(self):
        """Build a summary of the tests.

        This will construct a string describing the overall results
        of the test."""
        if self.testCount != 1:
            plural = "s"
        else:
            plural = ""
        return "{} failed from {} test{}".format(
            self.failCount, self.testCount, plural)
