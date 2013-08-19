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
from WellBehavedPython.api import *

class TestCaseTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)
        self.log = ""

    def before(self):
        self.log += "before "

    def after(self):
        self.log += "after "

    def ignoreError(self, error, errorType):
        pass

    def targetGoodMethod(self):
        """Target method when running unit tests."""
        self.log += "targetMethod "

    def targetFailedMethod(self):
        expect(True).toBeFalse()

    def targetErrorMethod(self):
        raise KeyError("asdf")

    def test_run_template_on_good_method(self):
        # we can't use self shunt here, because we need to
        # test for the after case. If we were self-shunting,
        # then after would be called after this test, which
        # would mean we couldn't test for it...
        test = TestCaseTests("targetGoodMethod")
        test.run(TestResults())
        
        expect(test.log).toEqual("before targetMethod after ")

    def test_run_template_on_error_method(self):
        # bypass usual error handling, because we want to
        # ingore it for this test
        test = TestCaseTests("targetErrorMethod")
        test.handleError = test.ignoreError
        results = TestResults()
        test.run(results)

        expect(test.log).toEqual("before after ")

    def test_run_template_on_ignored_method(self):
        test = TestCaseTests("targetGoodMethod")
        test.ignore = True

        test.run(TestResults())
        expect(test.log).toEqual("")

    def test_that_registerTestIgnored_called_if_test_ignored(self):
        # Where
        test = TestCaseTests("targetGoodMethod")
        test.ignore = True

        # When
        results = TestResults()
        test.run(results)

        # Then
        expect(results.testCount).toEqual(1)
        expect(results.passCount).toEqual(0)
        expect(results.failCount).toEqual(0)
        expect(results.errorCount).toEqual(0)
        expect(results.ignoredCount).toEqual(1)

    def test_that_registerTestPassed_called_if_test_passed(self):
        test = TestCaseTests("targetGoodMethod")
        results = TestResults()
        test.run(results)

        expect(results.testCount).toEqual(1)
        expect(results.failCount).toEqual(0)
        expect(results.passCount).toEqual(1)
        expect(results.errorCount).toEqual(0)
        expect(results.ignoredCount).toEqual(0)

    def test_that_registerTestFailed_called_if_test_failed(self):
        # Where
        test = TestCaseTests("targetFailedMethod")
        results = TestResults()
        test.handleError = self.ignoreError

        # When
        test.run(results)

        # Then
        expect(results.testCount).toEqual(1)
        expect(results.failCount).toEqual(1)
        expect(results.errorCount).toEqual(0)
        expect(results.passCount).toEqual(0)
        expect(results.ignoredCount).toEqual(0)

    def test_that_registerTestError_called_if_test_failed(self):
        # Where
        test = TestCaseTests("targetErrorMethod")
        results = TestResults()
        test.handleError = self.ignoreError

        # When
        test.run(results)

        # Then
        expect(results.testCount).toEqual(1)
        expect(results.failCount).toEqual(0)
        expect(results.errorCount).toEqual(1)
        expect(results.passCount).toEqual(0)        
        expect(results.ignoredCount).toEqual(0)

    def test_countTests_returns_1(self):
        # Where
        test = TestCaseTests("targetGoodMethod")
        
        # When

        # Then
        expect(test.countTests()).toEqual(1)
        
        
if __name__ == "__main__":
    # Let's hand craft a test suite

    suite = TestCaseTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())


