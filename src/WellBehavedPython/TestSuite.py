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

from .TestRunningException import *

class TestSuite:
    """Class for containing multiple tests.

    A TestSuite can contain anything that has a run method consistent
    with test case, so a full suite can be constructed out of other
    TestSuties and TestCases."""

    def __init__(self):
        """Constructor."""
        self.tests = []
        self.testClass = None
    
    def add(self, test):
        """Adds a test or other runnable to the suite.

        Inputs
        ------
        test : An object which has a run method consistent with
            TestCase.              
"""
        self._validateAddedTest(test)
        self.tests.append(test)

    def countTests(self):
        """Counts the active number of tests configured to run."""
        count = 0
        for test in self.tests:
            count += test.countTests()
        return count


    def run(self, results):
        """Runs all the tests in the suite."""
        for test in self.tests:
            test.run(results)        

    def _validateAddedTest(self, test):
        if self.testClass == None:
            self.testClass = type(test)
        else:
            if type(test) != self.testClass:
                raise TestRunningException("""Tests from two different test classes added to suite. 
To have a suite like this, create a suite with two sub-suites, one per test case class.""")



