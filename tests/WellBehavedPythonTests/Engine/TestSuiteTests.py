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

from WellBehavedPython.api import *
from WellBehavedPython.Engine.TestCase import *
from WellBehavedPython.Engine.TestRunningException import *
from WellBehavedPython.Engine.TestSuite import *

from .SampleTestCases import *

class TestSuiteTests(TestCase):

    def before(self):
        self.methodCalls = {}
        self.testMethodCount = 0
        self.suite = TestSuite("self.suite")
        self.results = TestResults()

    def after(self):
        TestCaseWithBeforeAndAfterClass.reset()

    def selfShuntIncrementMethod(self):
        self.testMethodCount += 1

    def selfShuntMethod(self):
        pass
        
    def test_running_suite_with_one_test_runs_one_test(self):
        # Where
        test = self.createTestSuiteTests("selfShuntIncrementMethod")
        test.configureTest('selfShuntIncrementMethod')
        self.suite.add(test)
        
        # When
        self.suite.run(self.results)

        # Then
        expect(test.testMethodCount).toEqual(1)
        expect(self.results.summary()).toMatch("0 failures.*1 test")

    def test_that_suite_with_one_test_counts_one_test(self):
        # Where
        test = self.createTestSuiteTests("selfShuntIncrementMethod")
        self.suite.add(test)

        # When

        # Then
        expect(self.suite.countTests()).toEqual(1)

    def test_running_suite_with_two_tests_runs_both(self):
        test1 = self.createTestSuiteTests("selfShuntIncrementMethod")
        test1.configureTest('selfShuntIncrementMethod');
        test2 = self.createTestSuiteTests("selfShuntMethod")
        test2.configureTest('selfShuntMethod')

        self.suite.add(test1)
        self.suite.add(test2)
        
        self.suite.run(self.results)

        expect(test1.countTests()).toEqual(1)
        expect(test2.countTests()).toEqual(1)
        expect(self.results.countTests()).toEqual(2)
        expect(self.results.countPasses()).toEqual(2)
        expect(self.results.summary()).toMatch("0 failures.*from 2 tests")

    def test_that_suite_with_two_tests_from_one_class_counts_both(self):
        # Where
        test1 = self.createTestSuiteTests("selfShuntIncrementMethod")
        test2 = self.createTestSuiteTests("selfShuntIncrementMethod")

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
        test1 = self.createTest(TestCaseWithPassingTest, "test_pass")
        test2 = self.createTest(TestCaseWithTwoPassingTests, "test_example1")
        suite = self.suite

        # When
        suite.add(test1)

        # Then
        expect(lambda: suite.add(test2)).toRaise(
            TestRunningException,
            expectedMessageMatches = "Tests from two different test classes added to suite")
        

    def test_that_suite_with_inner_suite_counts_all_subtests(self):
        # Where
        test1 = self.createTestSuiteTests("selfShuntIncrementMethod")
        test2 = self.createTestSuiteTests("selfShuntIncrementMethod")

        innerSuite = TestSuite("inner")
        innerSuite.add(test1)
        innerSuite.add(test2)

        self.suite.add(innerSuite)

        # When

        # Then
        expect(self.suite.countTests()).toEqual(2)


    def test_autosuite_discovers_correct_tests(self):
        suite = TestCaseWithTwoPassingTests.suite()
        expectedTestMethodNames = ["test_example1", "test_another_example" ];

        expect(suite.suiteName).toEqual("TestCaseWithTwoPassingTests")
        expect(len(suite.tests)).toEqual(2)
        for i in range(2):
            # we use naked asserts while waiting for isInstanceOf and
            # toBeIn
            message = "Test index {}".format(i)
            withUserMessage(message).expect(suite.tests[i]).toBeAnInstanceOf(TestCaseWithTwoPassingTests)
            withUserMessage(message).expect(suite.tests[i].testMethodName).toBeIn(expectedTestMethodNames)

    def test_autosuite_ingores_xtests(self):
        suite = TestCaseWithIgnoredTest.suite()
        expectedTestMethodNames = ["xtest_ignore"]

        expect(suite.suiteName).toEqual("TestCaseWithIgnoredTest")
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
        withUserMessage("beforeCalled should be false initially").expect(beforeAtStart).toBeFalse()
        withUserMessage("afterCalled should be false initially").expect(afterAtStart).toBeFalse()
        withUserMessage("beforeCalled should be true after calling beforeClass").expect(beforeAfterCallingBeforeClass).toBeTrue()
        withUserMessage("afterCalled should be false after calling afterClass").expect(afterAfterCallingAfterClass).toBeTrue()
        withUserMessage("beforeCalled should be false after calling reset()").expect(beforeAtEnd).toBeFalse()
        withUserMessage("beforeCalled should be false after calling reset()").expect(afterAtEnd).toBeFalse()

    def test_BeforeAndAfterCase_test_fails_if_before_not_called(self):
        # Where
        TestCaseWithBeforeAndAfterClass.reset()
        test = TestCaseWithBeforeAndAfterClass("test_statics")
        

        # Then
        results = TestResults()
        test.run(results)
        expect(results.countFaiulres()).toEqual(1, "beforeClass was not called")

    def test_BeforeAndAfterCase_test_fails_if_before_not_called(self):
        # Where
        TestCaseWithBeforeAndAfterClass.reset()
        test = self.createTest(TestCaseWithBeforeAndAfterClass, "test_statics")
        TestCaseWithBeforeAndAfterClass.beforeClass()
        TestCaseWithBeforeAndAfterClass.afterClass()
        
        # Then
        results = TestResults()
        test.run(results)
        withUserMessage("afterClass was called").expect(results.countFailures()).toEqual(1)

    def test_beforeAndAFterCase_test_passes_if_just_before_called(self):
        # Where
        TestCaseWithBeforeAndAfterClass.reset()
        test = self.createTest(TestCaseWithBeforeAndAfterClass, "test_statics")
        results = TestResults()

        # When
        TestCaseWithBeforeAndAfterClass.beforeClass()
        test.run(results)
        TestCaseWithBeforeAndAfterClass.afterClass()

        # Then
        withUserMessage("Test should pass").expect(results.countFailures()).toEqual(0)
        
    def test_suite_run_calls_beforeClass_before_any_tests_run(self):
        # Where
        TestCaseWithBeforeAndAfterClass.reset()
        suite = TestCaseWithBeforeAndAfterClass.suite()
        results = TestResults()

        # When
        suite.run(results)

        # Then
        withUserMessage("beforeClass should have been called"
                        ).expect(TestCaseWithBeforeAndAfterClass.beforeClassCalled).toBeTrue()


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
        expect(results.countErrors()).toEqual(0)
        withUserMessage(
            "failure would indicate afterClaass called too early"
            ).expect(results.countFailures()).toEqual(0)
        withUserMessage(
            "afterClass should have been called"
            ).expect(TestCaseWithBeforeAndAfterClass.afterClassCalled).toBeTrue()

    def createTest(self, klass, testMethod):
        test = klass()
        test.configureTest(testMethod)
        return test
            

    def test_error_in_beforeClass_marks_all_children_as_error(self):
        # Where
        suite = self.suite
        suite.add(self.createTest(TestCaseWithBeforeClassSaboteur, "test_statics"))
        suite.add(self.createTest(TestCaseWithBeforeClassSaboteur, "test_two"))

        # When
        results = TestResults()
        suite.run(results)

        # Then
        withUserMessage("both tests should count as failed").expect(results.countErrors()).toEqual(2)

    def test_error_in_afterClass_doesnt_mark_any_extra_errors(self):
        # Where
        suite = self.suite
        staticsSubsuite = self.createTest(TestCaseWithAfterClassSaboteur, "test_statics")

        otherSubsuite = self.createTest(TestCaseWithAfterClassSaboteur, "test_two")
        suite.add(staticsSubsuite)
        suite.add(otherSubsuite)

        # When
        results = TestResults()
        suite.run(results)

        # Then
        withUserMessage("both tests should count as passed").expect(results.countPasses()).toEqual(2)
        withUserMessage("but with an extra error anyway").expect(results.countErrors()).toEqual(1)
        withUserMessage("exception in afterClass is an error not a failure").expect(results.countFailures()).toEqual(0)

    def test_suite_run_calls_suite_started_suite_ended_on_initial_suite(self):
        # Where
        results = TestResults()
        spyOn(results.registerSuiteStarted)
        spyOn(results.registerSuiteCompleted)
        suite = TestCaseWithPassingTest.suite()
        testName = 'TestCaseWithPassingTest'

        # When
        suite.run(results)

        # Then
        expect(results.registerSuiteStarted).toHaveBeenCalledWith(testName)
        expect(results.registerSuiteCompleted).toHaveBeenCalledWith(testName)

    def test_suite_run_calls_run_using_subsuite(self):
        # Where
        results = TestResults()
        suite = TestCaseWithPassingTest.suite()

        # When
        suite.run(results)
        suiteResults = results.suiteResults[0]

        # Then
        expect(results.countTests()).toEqual(1)
        expect(suiteResults.countTests()).toEqual(1)

    def test_get_longest_description_for_suite_with_one_test(self):
        # Where
        suite = TestCaseWithPassingTest.suite()
        count = 0
        indentationPerCount = 3

        # When
        
        length = suite.getLongestDescriptionLength(count, indentationPerCount)

        # Then
        expect(length).toEqual(len("test_pass") + (1 + count) * indentationPerCount)

    def test_get_longest_description_for_suite_with_two_tests(self):
        # Where
        suite = TestCaseWithTwoPassingTests.suite()
        count = 0
        indentationPerCount = 3

        # When        
        length = suite.getLongestDescriptionLength(count, indentationPerCount)

        # Then
        expect(length).toEqual(len("test_another_example") + (1 + count) * indentationPerCount)

    def test_that_passing_subsuite_after_failing_subsuite_has_zero_errors(self):
        # Where
        wholeSuite = TestSuite("Outer")
        failingSubsuite = TestCaseWithFailingTest.suite()
        passingSubsuite = TestCaseWithPassingTest.suite()
        wholeSuite.add(failingSubsuite)
        wholeSuite.add(passingSubsuite)        

        # When
        results = TestResults()
        wholeSuite.run(results)
        wholeResults = results.suiteResults[0]


        # Then 
        withUserMessage("Should have two child results"
                        ).expect(len(wholeResults.suiteResults)).toEqual(2)
        failingResults = wholeResults.suiteResults[0]
        passingResults = wholeResults.suiteResults[1]

        withUserMessage("Failing results should contain one test").expect(failingResults.countTests()).toEqual(1)
        withUserMessage("Failing results should contain one failure").expect(failingResults.countFailures()).toEqual(1)
        withUserMessage("Passing results should contain one test").expect(passingResults.countTests()).toEqual(1)
        withUserMessage("Passing results should contain one failure").expect(passingResults.countPasses()).toEqual(1)
        withUserMessage("Passing results should contain no failures").expect(passingResults.countFailures()).toEqual(0)

    def createTestSuiteTests(self, testMethod):
        test = TestSuiteTests()
        test.configureTest(testMethod)
        return test
        


       

