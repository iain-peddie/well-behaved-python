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

import os
import os.path
import sys

from WellBehavedPython.TestCase import *
from WellBehavedPython.TestSuite import *
from WellBehavedPython.api import *
from WellBehavedPython.TestRunningException import *

from .SampleTestCases import *

class TestSuiteTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def before(self):
        self.testMethodCount = 0
        self.suite = TestSuite("self.suite")
        self.results = TestResults()

    def after(self):
        TestCaseWithBeforeAndAfterClass.reset()

    def selfShuntIncrementMethod(self):
        self.testMethodCount += 1
        
    def test_running_suite_with_one_test_runs_one_test(self):
        # Where
        test = TestSuiteTests("selfShuntIncrementMethod")
        self.suite.add(test)
        
        # When
        self.suite.run(self.results)

        # Then
        expect(test.testMethodCount).toEqual(1)
        expect(self.results.summary()).toMatch("0 failures.*1 test")

    def test_that_suite_with_one_test_counts_one_test(self):
        # Where
        test = TestSuiteTests("selfShuntIncrementMethod")
        self.suite.add(test)

        # When

        # Then
        expect(self.suite.countTests()).toEqual(1)
        

    def test_running_suite_with_two_tests_runs_both(self):
        test1 = TestSuiteTests("selfShuntIncrementMethod")
        test2 = TestSuiteTests("selfShuntIncrementMethod")

        self.suite.add(test1)
        self.suite.add(test2)
        
        self.suite.run(self.results)

        expect(test1.testMethodCount).toEqual(1)
        expect(test2.testMethodCount).toEqual(1)
        expect(self.results.summary()).toMatch("0 failures.*from 2 tests")

    def test_that_suite_with_two_tests_from_one_class_counts_both(self):
        # Where
        test1 = TestSuiteTests("selfShuntIncrementMethod")
        test2 = TestSuiteTests("selfShuntIncrementMethod")

        self.suite.add(test1)
        self.suite.add(test2)
        
        # When
        
        # Then
        expect(self.suite.countTests()).toEqual(2)        

    def test_that_suite_raises_error_if_tests_from_different_classes_added(self):
        # This may be transient behavior, but it makes getting going on
        # before and after easier. We want the suite to raise an exception
        # if additions to different classes are added to the same suite directly
        
        # Where 
        test1 = TestCaseWithPassingTest("test_pass")
        test2 = TestCaseWithTwoPassingTests("test_example1")
        suite = self.suite

        # When
        suite.add(test1)

        # Then
        expect(lambda: suite.add(test2)).toRaise(
            TestRunningException,
            expectedMessageMatches = "Tests from two different test classes added to suite")
        

    def test_that_suite_with_inner_suite_counts_all_subtests(self):
        # Where
        test1 = TestSuiteTests("selfShuntIncrementMethod")
        test2 = TestSuiteTests("selfShuntIncrementMethod")

        innerSuite = TestSuite("inner")
        innerSuite.add(test1)
        innerSuite.add(test2)

        self.suite.add(innerSuite)

        # When

        # Then
        expect(self.suite.countTests()).toEqual(2)


    def test_autosuite_discovers_correct_tests(self):
        suite = TestCaseWithTwoPassingTests.suite()
        expectedTestMethodNames = ["test_example1", "test_example2" ];

        # TODO : toHaveLength(2) ?
        expect(len(suite.tests)).toEqual(2)
        for i in range(2):
            # we use naked asserts while waiting for isInstanceOf and
            # toBeIn
            message = "Test index {}".format(i)
            expect(suite.tests[i]).toBeAnInstanceOf(TestCaseWithTwoPassingTests, message)
            expect(suite.tests[i].testMethodName).toBeIn(expectedTestMethodNames, message)

    def test_autosuite_ingores_xtests(self):
        suite = TestCaseWithIgnoredTest.suite()
        expectedTestMethodNames = ["xtest_ignore"]
        
        expect(len(suite.tests)).toEqual(len(expectedTestMethodNames))
        for test in suite.tests:
            expect(test.ignore).toBeTrue()
            expect(test).toBeAnInstanceOf(TestCaseWithIgnoredTest)
            expect(test.testMethodName).toBeIn(expectedTestMethodNames)

    def test_BeforeAndAfterCase_classmethods_set_static_variables(self):
        # This test checks the assumed behaviour of the test case that
        # will be called in other tests to ensure that the test is working
        # correctly
        
        # Where
        
        # (cache values to compare to later without drive-by-asserting)
        beforeAtStart = TestCaseWithBeforeAndAfterClass.beforeClassCalled
        afterAtStart = TestCaseWithBeforeAndAfterClass.afterClassCalled

        # When
        TestCaseWithBeforeAndAfterClass.beforeClass()
        TestCaseWithBeforeAndAfterClass.afterClass()

        beforeAfterCallingBeforeClass = TestCaseWithBeforeAndAfterClass.beforeClassCalled
        afterAfterCallingAfterClass = TestCaseWithBeforeAndAfterClass.afterClassCalled

        TestCaseWithBeforeAndAfterClass.reset()
        beforeAtEnd = TestCaseWithBeforeAndAfterClass.beforeClassCalled
        afterAtEnd = TestCaseWithBeforeAndAfterClass.afterClassCalled

        # Then
        expect(beforeAtStart).toBeFalse("beforeCalled should be false initially")
        expect(afterAtStart).toBeFalse("afterCalled should be false initially")
        expect(beforeAfterCallingBeforeClass).toBeTrue("beforeCalled should be true after calling beforeClass")
        expect(afterAfterCallingAfterClass).toBeTrue("afterCalled should be false after calling afterClass")
        expect(beforeAtEnd).toBeFalse("beforeCalled should be false after calling reset()")
        expect(afterAtEnd).toBeFalse("beforeCalled should be false after calling reset()")

    def test_BeforeAndAfterCase_test_fails_if_before_not_called(self):
        # Where
        TestCaseWithBeforeAndAfterClass.reset()
        test = TestCaseWithBeforeAndAfterClass("test_statics")
        

        # Then
        results = TestResults()
        test.run(results)
        expect(results.failCount).toEqual(1, "beforeClass was not called")

    def test_BeforeAndAfterCase_test_fails_if_before_not_called(self):
        # Where
        TestCaseWithBeforeAndAfterClass.reset()
        test = TestCaseWithBeforeAndAfterClass("test_statics")
        TestCaseWithBeforeAndAfterClass.beforeClass()
        TestCaseWithBeforeAndAfterClass.afterClass()
        
        # Then
        results = TestResults()
        test.run(results)
        expect(results.failCount).toEqual(1, "afterClass was called")

    def test_beforeAndAFterCase_test_passes_if_just_before_called(self):
        # Where
        TestCaseWithBeforeAndAfterClass.reset()
        test = TestCaseWithBeforeAndAfterClass("test_statics")
        results = TestResults()

        # When
        TestCaseWithBeforeAndAfterClass.beforeClass()
        test.run(results)
        TestCaseWithBeforeAndAfterClass.afterClass()

        # Then
        expect(results.failCount).toEqual(0, "Test should pass")
        
    def test_suite_run_calls_beforeClass_before_any_tests_run(self):
        # Where
        TestCaseWithBeforeAndAfterClass.reset()
        suite = TestCaseWithBeforeAndAfterClass.suite()
        results = TestResults()

        # When
        suite.run(results)

        # Then
        expect(TestCaseWithBeforeAndAfterClass.beforeClassCalled).toBeTrue(
            "beforeClass should have been called")

    def test_suite_run_calls_afterClass_after_tests_run(self):
        # Where
        TestCaseWithBeforeAndAfterClass.reset()
        suite = TestCaseWithBeforeAndAfterClass.suite()
        results = TestResults()

        # When
        # note : the test run asserts that afterClassCalled is
        # false when the test runs. This, combined with the asserts
        # in this test check that afterClass is called _after_
        # the test runs. With a do-nothing test, this would
        # not be possible
        suite.run(results)

        # Then
        expect(results.errorCount).toEqual(0)
        expect(results.failCount).toEqual(
            0, "failure would indicate afterClaass called too early")
        expect(TestCaseWithBeforeAndAfterClass.afterClassCalled).toBeTrue(
            "afterClass should have been called")

    def test_error_in_beforeClass_marks_all_children_as_error(self):
        # Where
        suite = self.suite
        suite.add(TestCaseWithBeforeClassSaboteur("test_statics"))
        suite.add(TestCaseWithBeforeClassSaboteur("test_two"))

        # When
        results = TestResults()
        suite.run(results)

        # Then
        expect(results.errorCount).toEqual(2, "both tests should count as failed")

    def test_error_in_afterClass_doesnt_mark_any_extra_errors(self):
        # Where
        suite = self.suite
        suite.add(TestCaseWithAfterClassSaboteur("test_statics"))
        suite.add(TestCaseWithAfterClassSaboteur("test_two"))

        # When
        results = TestResults()
        suite.run(results)

        # Then
        expect(results.passCount).toEqual(2, "both tests should count as passed")
        expect(results.errorCount).toEqual(1, "but with an extra error anyway")
        expect(results.failCount).toEqual(0, "exception in afterClass is an error not a failure")        
