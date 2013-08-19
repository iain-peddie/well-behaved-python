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
from WellBehavedPython.api import *

class TestResultsTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def before(self):
        self.results = TestResults()

    def test_summary_write_zero_numbers_correctly(self):
        results = self.results
        results.testCount = 0
        expect(results.summary()).toStartWith("0 failures 0 errors 0 ignored from 0 tests")

    def test_summary_writes_single_numbers_correctly(self):
        results = self.results
        results.testCount = 1
        results.failCount = 1
        results.passCount = 1
        results.errorCount = 1
        results.ignoredCount = 1
        
        expect(results.summary()).toStartWith("1 failure 1 error 1 ignored from 1 test")

    def test_summary_writes_plural_numbers_correctly(self):
        results = self.results
        results.testCount = 2
        results.failCount = 2
        results.passCount = 2
        results.errorCount = 2
        results.ignoredCount = 2
        expect(results.summary()).toStartWith("2 failures 2 errors 2 ignored from 2 tests")

    def test_summary_writes_stack_trace_correctly(self):
        results = self.results
        results.stackTraces = ["line1\n", "line2\n"]

        expect(results.summary()).toContain("""line1
line2
""")

    def test_register_test_started_increments_testCount(self):
        results = self.results
        before = results.testCount
        
        results.registerTestStarted()
        after = results.testCount

        expect(after).toEqual(before + 1)

    def test_register_test_passed_increments_passCount(self):
        results = self.results
        before = results.passCount
        
        results.registerTestPassed()
        after = results.passCount

        expect(after).toEqual(before + 1)

    def test_register_test_failed_increments_failCount_and_stores_stackTrace(self):
        results = self.results
        before = results.failCount
        
        results.registerTestFailed(["line1\n"])
        after = results.failCount

        expect(after).toEqual(before + 1)
        expect(results.stackTraces).toEqual(["line1\n"])
        
    def test_register_test_error_increments_failCount_and_stores_stackTrace(self):
        results = self.results
        before = results.errorCount
        
        results.registerTestError(["line1\n"])
        after = results.errorCount

        expect(after).toEqual(before + 1)
        expect(results.stackTraces).toEqual(["line1\n"])
        
    def test_register_test_ingored_increments_ingoredCount(self):
        results = self.results
        before = results.ignoredCount
        
        results.registerTestIgnored()
        after = results.ignoredCount

        expect(after).toEqual(before + 1)
        
        

if __name__ == "__main__":
    # Let's hand craft a test suite

    suite = TestResultsTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())
