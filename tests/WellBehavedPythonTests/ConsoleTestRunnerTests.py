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
#    but WITHOUT ANY WARRANTY; without even the impliedwarranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WellBehavedPython. If not, see <http://www.gnu.org/licenses/>.

from WellBehavedPython.api import *
from WellBehavedPython.Engine.TestCase import *
from WellBehavedPython.Runners.ConsoleTestRunner import *

from .Samples.SampleTestCases import *

import io
    
class ConsoleTestRunnerTests(TestCase):

    def before(self):
        self.output = io.StringIO()
        self.runner = ConsoleTestRunner(self.output, resultsPerLine = 3)

    def test_that_running_suite_with_no_tests_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestCaseWithNoTests.suite()

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("Starting test run of 0 tests")
        expect(self.output.getvalue()).toMatch(".*from 0 tests""")

        # Ignoring - this needs test completed event in test
        # runner and suteis to count number of tests
    def test_that_running_suite_with_one_tests_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestCaseWithPassingTest.suite()

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("""Starting test run of 1 test
\\.""")
        expect(self.output.getvalue()).toMatch(".*from 1 test""")
        
    def test_that_running_suite_with_two_passing_tests_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestSuite()
        suite.add(TestCaseWithPassingTest.suite())
        suite.add(TestCaseWithPassingTest.suite())

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toContain("""Starting test run of 2 tests
..
""")

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
        expect(self.output.getvalue()).toMatch("""test
F
""")

    def test_that_running_suite_with_one_failing_test_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestCaseWithErrorTest.suite()

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("""test
E
""")

    def test_that_running_suite_with_one_ignored_test_produces_correct_output(self):
        # Where
        runner = self.runner
        suite = TestCaseWithIgnoredTest.suite()

        # When
        results = runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("""test
I
""")
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

        # When
        runner.run(suite)

        # Then
        expect(self.output.getvalue()).toMatch("""tests
.FE
""")
        
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
        expect(theOutput).toContain("""
F.
""")
        expect(theOutput).toMatch("F\\.")
        expect(theOutput).toMatch(""".*from 2 tests.*
Failing test
.*File.*\\.py""")

    def test_that_runner_limits_results_block_width(self):
        # Where
        runner = self.runner
        suite = TestSuite()
        for i in range(0,4):
            suite.add(TestCaseWithPassingTest.suite())
        suite.add(TestCaseWithFailingTest.suite())
        suite.add(TestCaseWithErrorTest.suite())

        # When
        runner.run(suite)

        # Then
        theOutput = self.output.getvalue()
        expect(theOutput).toContain("""...
.FE
""")
        expect(theOutput).toContain("from 6 tests")

