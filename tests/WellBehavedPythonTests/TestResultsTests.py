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
        results._testCount = 1
        results._failCount = 1
        results._passCount = 1
        results._errorCount = 1
        results._ignoredCount = 1
        
        expect(results.summary()).toStartWith("1 failure 1 error 1 ignored from 1 test")

    def test_summary_writes_plural_numbers_correctly(self):
        results = self.results
        results._testCount = 2
        results._failCount = 2
        results._passCount = 2
        results._errorCount = 2
        results._ignoredCount = 2
        expect(results.summary()).toStartWith("2 failures 2 errors 2 ignored from 2 tests")

    def test_summary_writes_stack_trace_correctly(self):
        results = self.results
        results.stackTraces = ["line1\n", "line2\n"]

        expect(results.summary()).toContain("""line1
line2
""")

    def test_summary_writes_duration(self):
        results = self.results
        # Where
        result = results.registerTestStarted("suite", "test")
        results.registerTestPassed("suite", "test")
        result.EndTime = result.StartTime + timedelta(minutes = 1)

        # When
        
        # Then
        expect(results.summary()).toMatch("in 60\\.0+s")

    def test_register_test_started_increments_testCount(self):
        results = self.results
        before = results.countTests()
        
        results.registerTestStarted("suite", "test")
        after = results.countTests()

        expect(after).toEqual(before + 1)

    def test_register_test_passed_increments_passCount(self):
        results = self.results
        results.registerTestStarted("suite", "test")
        before = results.countPasses()
        
        results.registerTestPassed("suite", "test")
        after = results.countPasses()

        expect(after).toEqual(before + 1)

    def test_register_test_failed_increments_failCount_and_stores_stackTrace(self):
        results = self.results
        before = results.countFailures()
        results.registerTestStarted("suite", "test")
        
        results.registerTestFailed("suite", "test", ["line1\n"])
        after = results.countFailures()

        expect(after).toEqual(before + 1)
        expect(results.stackTraces).toEqual(["line1\n"])
        
    def test_register_test_error_increments_failCount_and_stores_stackTrace(self):
        results = self.results
        before = results.countErrors()
        results.registerTestStarted("suite", "test")
        
        results.registerTestError("suite", "test", ["line1\n"])
        after = results.countErrors()

        expect(after).toEqual(before + 1)
        expect(results.stackTraces).toEqual(["line1\n"])
        
    def test_register_test_ingored_increments_ingoredCount(self):
        results = self.results
        results.registerTestStarted("suite", "test")
        before = results.countIgnored()
        
        results.registerTestIgnored("suite", "test")
        after = results.countIgnored()

        expect(after).toEqual(before + 1)

    def test_result_passes_updates_result(self):
        # Where
        results = self.results
        result = results.registerTestStarted("suite", "test")

        # When
        results.registerTestPassed("suite", "test")

        # Then
        expect(result.getDuration()).toBeGreaterThan(timedelta())
        expect(results.getDuration().total_seconds()).toEqual(
            result.getDuration().total_seconds())

    def test_result_fails_updates_result(self):
        # Where
        results = self.results
        result = results.registerTestStarted("suite", "test")

        # When
        results.registerTestFailed("suite", "test", ["stacktrace"])

        # Then
        expect(result.getDuration()).toBeGreaterThan(timedelta())
        expect(results.getDuration().total_seconds()).toEqual(
            result.getDuration().total_seconds())
        
    def test_result_error_updates_result(self):
        # Where
        results = self.results
        result = results.registerTestStarted("suite", "test")

        # When
        results.registerTestError("suite", "test", ["stacktrace"])

        # Then
        expect(result.getDuration()).toBeGreaterThan(timedelta())
        expect(results.getDuration().total_seconds()).toEqual(
            result.getDuration().total_seconds())

        
    def test_result_ignored_updates_result(self):
        # Where
        results = self.results
        result = results.registerTestStarted("suite", "test")

        # When
        results.registerTestIgnored("suite", "test")

        # Then
        expect(result.getDuration()).toBeGreaterThan(timedelta())
        expect(results.getDuration().total_seconds()).toEqual(
            result.getDuration().total_seconds())

    def test_registerSuiteStarted_returns_child_results(self):
        # Where
        results = self.results

        # When
        childResults = results.registerSuiteStarted("suite")        
        childResults.registerTestStarted("suite", "test_something")
        childResults.registerTestPassed("suite", "test_something")
        results.registerSuiteCompleted("suite")

        # Then
        expect(childResults.countTests()).toEqual(1)
        expect(results.countTests()).toEqual(1)
        expect(results.getDuration()).toBeGreaterThanOrEqualTo(childResults.getDuration())

    def test_passing_method_in_subsuite_counted_in_parent(self):
        # Where
        results = self.results

        # When
        childResults = results.registerSuiteStarted("subsuite")
        childResults.registerTestStarted("subsuite", "passing")
        childResults.registerTestPassed("subsuite", "passing")
        results.registerSuiteCompleted("subsuite")

        # Then
        expect(results.countTests()).toEqual(1)
        expect(results.countPasses()).toEqual(1)

    def test_failed_methods_counted_in_parent(self):
        # Where
        results = self.results

        # When
        childResults = results.registerSuiteStarted("subsuite")
        childResults.registerTestStarted("subsuite", "failing")
        childResults.registerTestFailed("subsuite", "failing", ["fail stack"])
        results.registerSuiteCompleted("subsuite")

        # Then
        expect(results.countTests()).toEqual(1)
        expect(results.countPasses()).toEqual(0)
        expect(results.countFailures()).toEqual(1)
        expect(results.getStackTraces()).toEqual(["fail stack"])

    def test_failed_methods_counted_in_parent(self):
        # Where
        results = self.results

        # When
        childResults = results.registerSuiteStarted("subsuite")
        childResults.registerTestStarted("subsuite", "error")
        childResults.registerTestError("subsuite", "error", ["error stack"])
        results.registerSuiteCompleted("subsuite")

        # Then
        expect(results.countTests()).toEqual(1)
        expect(results.countPasses()).toEqual(0)
        expect(results.countFailures()).toEqual(0)
        expect(results.countErrors()).toEqual(1)
        expect(results.getStackTraces()).toEqual(["error stack"])

    def test_ignored_methods_counted_in_parent(self):
        # Where
        results = self.results

        # When
        childResults = results.registerSuiteStarted("subsuite")
        childResults.registerTestStarted("subsuite", "ignored")
        childResults.registerTestIgnored("subsuite", "ignored")
        results.registerSuiteCompleted("subsuite")

        # Then
        expect(results.countTests()).toEqual(1)
        expect(results.countPasses()).toEqual(0)
        expect(results.countFailures()).toEqual(0)
        expect(results.countErrors()).toEqual(0)
        expect(results.countIgnored()).toEqual(1)

    def test_summart_summarises_children(self):
        # Where
        results = self.results

        # When
        childResults = results.registerSuiteStarted("subsuite")
        childResults.registerTestStarted("subsuite", "passing")
        childResults.registerTestPassed("subsuite", "passing")
        childResults.registerTestStarted("subsuite", "failing")
        childResults.registerTestFailed("subsuite", "failing", ["fail stack"])
        childResults.registerTestStarted("subsuite", "error")
        childResults.registerTestError("subsuite", "error", ["error stack"])
        childResults.registerTestStarted("subsuite", "ignored")
        childResults.registerTestIgnored("subsuite", "ignored")
        results.registerSuiteCompleted("subsuite")
        
        # Then
        summary = results.summary()
        expect(summary).toContain("1 failure")
        expect(summary).toContain("1 error")
        expect(summary).toContain("1 ignored")
        expect(summary).toContain("from 4 tests")
        expect(summary).toContain("fail stack")
        expect(summary).toContain("error stack")
