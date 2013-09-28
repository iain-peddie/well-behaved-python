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

from WellBehavedPython.api import *
from WellBehavedPython.TestCase import *
from WellBehavedPython.VerboseConsoleTestRunner import *

from .SampleTestCases import *

import io

class VerboseConsoleTestRunnerTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def before(self):
        self.output = io.StringIO()
        self.runner = VerboseConsoleTestRunner(self.output)

    def test_setup(self):
        pass

    def test_that_running_suite_with_no_tests_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestCaseWithNoTests.suite()

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("Starting test run of 0 tests")
        expect(self.output.getvalue()).toMatch(".*from 0 tests""")

    def test_that_running_suite_with_one_tests_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestCaseWithPassingTest.suite()

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("Starting test run of 1 test")
        expect(self.output.getvalue()).toMatch("from 1 test")
        expect(self.output.getvalue()).toMatch("test_pass.* passed in [0-9\\.]+s")
        
    def test_that_running_suite_with_two_passing_tests_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestSuite()
        suite.add(TestCaseWithPassingTest.suite())
        suite.add(TestCaseWithPassingTest.suite())

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("Starting test run of 2 tests")
        expect(self.output.getvalue()).toMatch("from 2 tests")
        expect(self.output.getvalue()).toMatch("""
 *test_pass.* passed in [0-9\\.]+s""")
        

    def test_that_runner_returns_test_result(self):
        # Where
        runner = self.runner
        suite = TestCaseWithPassingTest.suite();

        # When
        results = runner.run(suite)

        # Then
        expect(results.countPasses()).toEqual(1)
        expect(results.countTests()).toEqual(1)

    def test_that_running_suite_with_one_failing_test_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestCaseWithFailingTest.suite()

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("Starting test run of 1 test")
        expect(self.output.getvalue()).toMatch("from 1 test")
        expect(self.output.getvalue()).toMatch("test_fail.* failed in [0-9\\.]+s")

    def test_that_running_suite_with_one_error_test_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestCaseWithErrorTest.suite()

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("Starting test run of 1 test")
        expect(self.output.getvalue()).toMatch("from 1 test")
        expect(self.output.getvalue()).toMatch("test_error.* error in [0-9\\.]+s")

    def test_that_running_suite_with_one_ignored_test_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestCaseWithIgnoredTest.suite()

        # When
        results = runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("Starting test run of 1 test")
        expect(self.output.getvalue()).toMatch("from 1 test")
        expect(self.output.getvalue()).toMatch("test_ignore.* ignored in [0-9\\.]+s")
        expect(results.countIgnored()).toEqual(1)
        expect(results.countTests()).toEqual(1)
        expect(results.countPasses()).toEqual(0)

    def test_that_runner_can_cope_with_one_of_each(self):
        # Where
        runner = self.runner
        suite = TestSuite()
        suite.add(TestCaseWithPassingTest.suite())
        suite.add(TestCaseWithFailingTest.suite())
        suite.add(TestCaseWithErrorTest.suite())
        suite.add(TestCaseWithIgnoredTest.suite())

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("4 tests")
        expect(self.output.getvalue()).toMatch("test_pass.*passed")
        expect(self.output.getvalue()).toMatch("test_fail.*failed")
        expect(self.output.getvalue()).toMatch("test_error.*error")
        expect(self.output.getvalue()).toMatch("test_ignore.*ignored")
        
    def test_that_runner_buffers_output_and_prints_after_tests(self):
        # Where
        runner = self.runner
        suite = TestSuite()
        suite.add(TestCaseWithFailingTest.suite())
        suite.add(TestCaseWithPassingTest.suite())

        # When
        runner.run(suite)

        # Then
        theOutput = self.output.getvalue()
        expect(theOutput).toContain("failed")
        expect(theOutput).toContain("passed")
        expect(theOutput).toMatch(""".*from 2 tests.*
Failing test
.*File.*\\.py""")

    def test_that_runner_prints_suite_name_on_suite_entry(self):
        # Where
        runner = self.runner
        runner.results = TestResults()
        runner.suite = TestSuite()
        runner.suite.getLongestDescriptionLength = lambda nestingCount, intendationPerCount: 50
        
        # When
        runner.registerSuiteStarted("subSuiteName")

        # Then
        theOutput = self.output.getvalue()
        expect(theOutput).toMatch("""subSuiteName\\.+
""")

    def test_that_runner_prints_suite_passed_and_time_on_suite_exit(self):
        # Where
        suiteName = "subSuiteName"
        runner = self.runner
        results = TestResults()
        results.registerSuiteStarted(suiteName)
        results.registerTestStarted(suiteName, "test")
        results.registerTestPassed(suiteName, "test")
        runner.results = results

        # When
        runner.registerSuiteCompleted(suiteName)
        
        # Then
        theOutput = self.output.getvalue()
        expect(theOutput).toMatch("subSuiteName.* passed in [0-9][\\.0-9]*s")

    def test_that_runner_prints_test_failed_on_suite_exit_if_one_test_failed(self):
        # Where
        suiteName = "subSuiteName"
        runner = self.runner
        results = TestResults()
        results.registerSuiteStarted(suiteName)
        results.registerTestStarted(suiteName, "test")
        results.registerTestFailed(suiteName, "test", ["mock", "stack", "trace"])
        runner.results = results

        # When
        runner.registerSuiteCompleted(suiteName)
        
        # Then
        theOutput = self.output.getvalue()
        expect(theOutput).toMatch("subSuiteName.* failed in [0-9][\\.0-9]*s")

    def test_subsuites_indented_relative_to_parent(self):
        # Where
        outerSuite = TestSuite("OuterTestSuite")
        innerSuite = TestCaseWithPassingTest.suite()
        outerSuite.add(innerSuite)

        runner = self.runner

        # When
        runner.run(outerSuite)

        # Then
        theOutput = self.output.getvalue()
        expect(theOutput).toMatch("\n   TestCaseWithPassingTest")
        expect(theOutput).toMatch("\n      test_pass")
        expect(theOutput).toMatch("\nOuterTestSuite\\.+ passed")

    def test_that_tests_indented_to_equal_levels(self):
        # Where
        suite = TestCaseWithTwoPassingTests.suite()
        runner = self.runner

        # When
        runner.run(suite)

        # Then
        theOutput = self.output.getvalue()
        expect(theOutput).toContain("   test_example1..........");
        expect(theOutput).toContain("   test_another_example...");

    def test_that_suites_dotted_to_sample_level_as_tests(self):
        # Where
        suite = TestCaseWithLongTestName.suite()
        runner = self.runner
        runner.suite = suite
        runner._updateDotsLevel()

        # When
        runner.run(suite)

        # Then
        theOutput = self.output.getvalue()
        expect(theOutput).toContain("TestCaseWithLongTestName.................................\n");
        expect(theOutput).toContain("TestCaseWithLongTestName................................. passed");
        expect(theOutput).toContain("   test_case_with_test_name_longer_than_test_case_name... passed");

