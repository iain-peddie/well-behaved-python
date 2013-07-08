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

from WellBehavedPython.TestCase import *
from WellBehavedPython.TestResults import *
from WellBehavedPython.TestSuite import *
from WellBehavedPython.Expect import *

class TestResultsTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def before(self):
        self.results = TestResults()
        self.results.registerTestStarted()

    def test_summary_for_single_passing_test(self):
        results = self.results

        Expect(results.summary()).toEqual("0 failed from 1 test")

    def test_summary_for_two_passing_tests(self):
        results = self.results
        results.registerTestStarted()

        Expect(results.summary()).toEqual("0 failed from 2 tests")

    def test_summary_for_single_failing_test(self):
        results = self.results
        results.registerTestFailed()

        Expect(results.summary()).toEqual("1 failed from 1 test")

    def test_summary_for_passing_and_failing_test(self):
        results = self.results
        results.registerTestFailed()
        results.registerTestStarted()

        Expect(results.summary()).toEqual("1 failed from 2 tests")

if __name__ == "__main__":
    # Let's hand craft a test suite

    suite = TestResultsTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())
