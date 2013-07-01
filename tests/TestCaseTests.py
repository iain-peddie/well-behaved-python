#!/usr/bin/env python3

# Copyright 2013 Iain Peddie inr314159@hotmail.com
# 
#    This file is part of WellBehavedPython
#
#    WellBehavedPython is free softwaree: you can redistribute it and/or modify
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
from WellBehavedPython.Expect import *

class TestCaseTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)
        self.log = ""

    @staticmethod
    def suite():
        testMethods = [
            "test_run_template_on_good_method", 
            "test_run_template_on_error_method", 
            "test_good_method_summary",
            "test_error_method_summary"
            ]
        
        suite = TestSuite()
    
        for testMethod in testMethods:
            suite.add(TestCaseTests(testMethod))
        
        return suite

    def before(self):
        self.log += "before "

    def after(self):
        self.log += "after "

    def ignoreError(self, error):
        pass

    def targetGoodMethod(self):
        """Target method when running unit tests."""
        self.log += "targetMethod "

    def targetErrorMethod(self):
        raise Exception

    def test_run_template_on_good_method(self):
        # we can't use self shunt here, because we need to
        # test for the after case. If we were self-shunting,
        # then after would be called after this test, which
        # would mean we couldn't test for it...
        test = TestCaseTests("targetGoodMethod")
        test.run(TestResults())
        
        Expect(test.log).toEqual("before targetMethod after ")

    def test_run_template_on_error_method(self):
        # bypass usual error handling, because we want to
        # ingore it for this test
        test = TestCaseTests("targetErrorMethod")
        test.handleError = test.ignoreError
        test.run(TestResults())

        Expect(test.log).toEqual("before after ")

    def test_good_method_summary(self):
        test = TestCaseTests("targetGoodMethod")
        results = TestResults()
        test.run(results)
        
        Expect(results.summary()).toEqual("0 failed from 1 test")

    def test_error_method_summary(self):
        test = TestCaseTests("targetErrorMethod")
        test.handleError = test.ignoreError
        results = TestResults()

        test.run(results)

        Expect(results.summary()).toEqual("1 failed from 1 test")
        
        
if __name__ == "__main__":
    # Let's hand craft a test suite

    suite = TestCaseTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())


